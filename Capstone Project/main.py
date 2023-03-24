import settings
import parameters_window
import tkinter

if __name__ == "__main__":
    organisms = []
    root = tkinter.Tk()
    root.minsize(settings.screen_size, settings.screen_size//2)
    parameters_window.center_window(root)
    root.winfo_toplevel().title("A-Life Challenge")

    parameters_window.change_to_parameters(root,
                                           organisms,
                                           settings.prey_attributes,
                                           settings.pred_attributes,
                                           True)  # initial call of parameters_window
    root.mainloop()
