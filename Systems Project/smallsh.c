#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <unistd.h>
#include <sys/wait.h>
#include <fcntl.h>
#include <signal.h>

/*
* Structure to hold components of a shell command
* Stores command name, a pointer to a pointer to the first char of an arg in an array of args
* Stores any user specified filenames for input/output redirection 
* and a bool which is true if the process is directed to the background
*/
struct command {
  char *name;
  char **args;
  char *input;
  char *output;
  bool bg;
  struct command *next;
};

/*
* Citation for the following funciton:
* Date: 10/28/21
* Copied from:
* Source URL: https://stackoverflow.com/a/3069580
*/
int lenHelper(unsigned x) {
    if (x >= 1000000000) return 10;
    if (x >= 100000000)  return 9;
    if (x >= 10000000)   return 8;
    if (x >= 1000000)    return 7;
    if (x >= 100000)     return 6;
    if (x >= 10000)      return 5;
    if (x >= 1000)       return 4;
    if (x >= 100)        return 3;
    if (x >= 10)         return 2;
    return 1;
}

/*
* Citation for the following funciton:
* Date: 10/28/21
* Copied and adapted from:
* Source URL: https://stackoverflow.com/a/779960
*/
char *varExp(char *orig) {
  char *rep;    
  rep = "$$";   //variable to be expanded
  int pid = getpid(); //get pid of shell
  char *with = malloc(lenHelper(pid)+1);  
  sprintf(with, "%d", pid); //convert pid to string for replacing $$
  char *result; //the return string
  char *ins;    //the next insert point
  char *tmp;    //varies
  int len_rep;  //ength of rep (the string to remove)
  len_rep = strlen(rep);
  int len_with; //length of with (the string to replace rep with)
  len_with = strlen(with);
  int len_front; //distance between rep and end of last rep
  int count;    //number of replacements
  //count the number of replacements needed
  ins = orig;
  for (count = 0; (tmp = strstr(ins, rep)); ++count) {
      ins = tmp + len_rep;
  }
  tmp = result = malloc(strlen(orig) + (len_with - len_rep) * count + 1);
  if (!result)
      return NULL;

  //first time through the loop, all the variable are set correctly
  //from here on,
  //  tmp points to the end of the result string
  //  ins points to the next occurrence of rep in orig
  //  orig points to the remainder of orig after "end of rep"
  while (count--) {
      ins = strstr(orig, rep);
      len_front = ins - orig;
      tmp = strncpy(tmp, orig, len_front) + len_front;
      tmp = strcpy(tmp, with) + len_with;
      orig += len_front + len_rep; //move to next "end of rep"
  }
  strcpy(tmp, orig);
  return result;
}

/*
* Signal handler for SIGTSTP (CTRL+Z)
*/
void handle_SIGTSTP(int signo){
  if (getenv("FG")) { //if we are currently in fg only mode, exit
    unsetenv("FG");
    char *message = "\nExiting foreground-only mode\n";
    write(STDOUT_FILENO, message, 33);
  } else {  //enter fg mode by creation of FG environmental variable
    setenv("FG", "1", 0);
    char *message = "\nEntering foreground-only mode (& is now ignored)\n";
    write(STDOUT_FILENO, message, 53);
  }
}

/*
* Displays command-line prompt to user and gets the user input string contianing the command
* Parses the user input string, exiting if input is a comment (# 1st char) or blank line
* Parses command into the command strcut currC representing the current command
* If the command name is a builting command (exit, cd, or status) completes the corresponding task directly
* Otherwise, forks a new process and locates the executable with the specified name in the PATH environment
* Completes any specified IO redirection and runs the command in a child process via exec()
* Foreground processes are waited for by the parent (no new prompt until terminates)
* Background processes display messages when started and terminated but are not waited for by parent 
*/
int prompt(pid_t *bgList, int *bgCount) {
  //initialize command string and obtain from user
  char *cStr;
  char *newargv[512] = {NULL};  //init array to hold name and arguments for execvp
  cStr = calloc(2048, sizeof(char));
  printf(": ");
  fflush(stdout);
  fgets(cStr, 2048, stdin);
  //replace newline from fgets with null terminator
  cStr[strcspn(cStr, "\n")] = 0;
  //perform variable expansion on instances of $$
  cStr = varExp(cStr);
  //parse command string into strcuture
  struct command *currC = malloc(sizeof(struct command));
  currC->args = calloc(512, sizeof(char *)); //init args array
  currC->bg = 0; //init to foreground
  int i = 0; //init args array index to first

  //first token is required name of command or will indicate comment
  char *token = strtok(cStr, " ");
  if (token == NULL) {
    printf("\n");
    fflush(stdout);
    return 0;
  }
  if (strncmp(token, "#", 1) == 0) {
    printf("\n");
    fflush(stdout);
    return 0;
  } else {
    currC->name = calloc(strlen(token)+1, sizeof(char));
    strcpy(currC->name, token);
    newargv[0] = calloc(strlen(token)+1, sizeof(char));
    strcpy(newargv[0], token);
  }

  token = strtok(NULL, " ");
  //parse optional parameters
  while (1) {
    if (token == NULL) {
      break;
    }
    //check for input or output redirection or background
    if (strncmp(token, "<", 1) == 0) {
      //parse new input location & add to struct
      token = strtok(NULL, " ");
      currC->input = calloc(strlen(token) + 1, sizeof(char));
      strcpy(currC->input, token);
    } else if (strncmp(token, ">", 1) == 0){
      //parse new output location & add to struct
      token = strtok(NULL, " ");
      currC->output = calloc(strlen(token) + 1, sizeof(char));
      strcpy(currC->output, token);
    } else if (strncmp(token, "&", 1) == 0) {
      currC->bg = 1; 
      //if command to be run in background and we're not in fg only mode
      if (getenv("FG") == NULL) {  
        //if no specified input redirection, redirect input to /dev/null
        if (currC->input == NULL) {
          currC->input = "/dev/null";
        }
        //if no specified output redirection, redirect output to /dev/null
        if (currC->output == NULL) {
          currC->output = "/dev/null";
        }
      }
    //if no <,>,& must be in the args list
    } else {
      //allocate necessary size of array element
      currC->args[i] = calloc(strlen(token)+1, sizeof(char));
      strcpy(currC->args[i], token);
      newargv[i+1] = calloc(strlen(token)+1, sizeof(char));
      strcpy(newargv[i+1], token);
      i++;
    }
    //next token 
    token = strtok(NULL, " ");
  }
  currC->args[i] = NULL; //terminate args array with NULL for use with execvp

  int childStatus;
  //decision tree for built in commands vs others
  if (strcmp(currC->name, "exit") == 0) {
    // user wishes to terminate the shell
    exit(0);
    return 1;
    //user changes working directory
  } else if (strcmp(currC->name, "cd") == 0) {
    if (currC->args[0]) {
      chdir(currC->args[0]);
    } else {
      chdir(getenv("HOME"));
    }
    //user checks status of last fg process or 0 if none
  } else if (strcmp(currC->name, "status") == 0) {
    if (WIFEXITED(childStatus)) {
        printf("exit status %d\n", WEXITSTATUS(childStatus));
        fflush(stdout);
    } else {
      printf("exit status 0\n");
      fflush(stdout);
    }

    //FOR NON-BUILTIN COMMANDS
  } else {
    //fork child process for running of non-builtin command
    pid_t childPid = fork();
    if(childPid == -1){
      perror("fork() failed!\n");
      fflush(stdout);
      exit(1);

    } else if(childPid == 0){
      //the child process executed this branch;
      struct sigaction SIGTSTP_action = {{0}};
      SIGTSTP_action.sa_handler = SIG_IGN;
      sigaction(SIGTSTP, &SIGTSTP_action, NULL);   //all child processes ignore ^Z
      //handle IO redirects if present in command
      if (currC->input) {
        int sourceFD = open(currC->input, O_RDONLY);  //open input file for reading
        if (sourceFD == -1) { 
          printf("cannot open %s for input\n", currC->input); 
          fflush(stdout);
          childStatus = 1; //set exit status to 1 without exiting
        }
        dup2(sourceFD, 0);  //redirect stdin to sourceFD
      }
      if (currC->output) {
        int targetFD = open(currC->output, O_WRONLY | O_CREAT | O_TRUNC, 0666); //open input file for writing
        if (targetFD == -1) { 
          printf("cannot open %s for output\n", currC->output);
          fflush(stdout);
          childStatus = 1; //set exit status to 1 without exiting
        }
        dup2(targetFD, 1); //redirect stdout to targetFD
      }
      if (currC->bg == 0) { //if a foreground child process, restore default SIGINT action
        struct sigaction SIGINT_action = {{0}};
        SIGINT_action.sa_handler = SIG_DFL;
        sigaction(SIGINT, &SIGINT_action, NULL);
      }

      //populate array for execvp with filename, vector of args, and NULL
      execvp(newargv[0], newargv);
      //only if execvp fails due to no such file
      printf("%s: no such file or directory\n", currC->name);
      fflush(stdout);   
	    exit(1);

    } else{
      //the parent process executes this branch
      //either wait for child in foreground to finish execution or non-blocking wait with background
      if (currC->bg == 1) { //if directed to background with &
        printf("background pid is %d\n", childPid);
        fflush(stdout); 
        pid_t bgChild = childPid;
        bgList[*bgCount] = bgChild;  //add pid to the list of background processes
        (*bgCount)++; //increment count of active bg processes
          //check status of background processes and print message for those that have terminated normally
        for (int i=0; i < *bgCount; i++) {
          if (bgList[i] != -1) {
            waitpid(bgList[i], &childStatus, WNOHANG);
            if (WIFEXITED(childStatus)) {  
              printf("background pid %d is done: exit value %d\n", bgList[i], WEXITSTATUS(childStatus));
              fflush(stdout); 
              bgList[i] = -1;   //clear pid from index to indicate it is terminated normally
            } else if (WIFSIGNALED(childStatus)) {
              printf("terminated by signal %d\n", WTERMSIG(childStatus));
              fflush(stdout);
              bgList[i] = -1;   //clear pid from index to indicate it is terminated abnormally
            }
          }
        }
      } else {
        childPid = waitpid(childPid, &childStatus, 0);
      }
    }
  }
  free(currC);
  return 0;
}

int main(void) {
  struct sigaction SIGINT_action = {{0}}, SIGTSTP_action = {{0}};
  SIGINT_action.sa_handler = SIG_IGN;
  SIGTSTP_action.sa_handler = handle_SIGTSTP;
  SIGINT_action.sa_flags = SA_RESTART;
  SIGTSTP_action.sa_flags = SA_RESTART;
  sigaction(SIGINT, &SIGINT_action, NULL);  //set parent to ignore ^C
  sigaction(SIGTSTP, &SIGTSTP_action, NULL);  //custom handler for parent process ^Z
  //init linked list of commands for bg processes
  pid_t bgList[10]; //stores the pids of currently running background processes
  int *bgCount;   //stores the count of currently running background processes
  int i = 0;
  bgCount = &i;
  int result = 0;
  while (result == 0) {
    result = prompt(bgList, bgCount); //pass in array of background process pids and the count
  }
  return 0;
}