const express = require('express');
const app = express();
app.enable('trust proxy');

const {Datastore} = require('@google-cloud/datastore');

const bodyParser = require('body-parser');
const request = require('request');

const datastore = new Datastore();

const jwt = require('express-jwt');
const jwksRsa = require('jwks-rsa');

const ATHLETES = "Athletes";
const RACES = "Races";
const COURSES = "Courses";
const INVALID_CHARS = /[`!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?~]/;
const MAX_LEN = 64;

const router = express.Router();
const login = express.Router();

// Generated from Auth0
const CLIENT_ID = '';
const CLIENT_SECRET = '';
const DOMAIN = '';

app.use(bodyParser.json());

function fromDatastore(item){
    item.id = item[Datastore.KEY].id;
    return item;
}

const checkJwt = jwt({
  secret: jwksRsa.expressJwtSecret({
    cache: true,
    rateLimit: true,
    jwksRequestsPerMinute: 5,
    jwksUri: `https://${DOMAIN}/.well-known/jwks.json`
  }),

  // Validate the audience and the issuer.
  issuer: `https://${DOMAIN}/`,
  algorithms: ['RS256']
});

/* ------------- Begin Athlete Model Functions ------------- */
function post_athlete(sub) {
  var key = datastore.key(ATHLETES);
  const new_athlete = { "first_name": null, "last_name": null, "age": null, "school" : null, "races": [], "sub_id": sub};
  return datastore.save({ "key": key, "data": new_athlete }).then(() => { return key });
}

function patch_athlete(athlete_id, body) {
  const key = datastore.key([ATHLETES, parseInt(athlete_id, 10)]);
  return datastore.get(key).then((entity) => {
    if (entity[0] === undefined || entity[0] === null) {
      return entity;
    } else {
      const data = entity.map(fromDatastore);
      if (body.first_name) {
        data[0].first_name = body.first_name;
      }
      if (body.last_name) {
        data[0].last_name = body.last_name;
      }
      if (body.age) {
        data[0].age = body.age;
      }
      if (body.school) {
        data[0].school = body.school;
      }
      return datastore.save({ "key": key, "data": data[0] }).then(() => { return key });
    }
  });
}

function get_athlete(athlete_id, req) {
  const key = datastore.key([ATHLETES, parseInt(athlete_id, 10)]);
    return datastore.get(key).then((entity) => {
      if (entity[0] === undefined || entity[0] === null) {
        return entity;
      } else {
        var athlete = entity.map(fromDatastore);
        athlete[0].self = req.protocol + "://" + req.get("host") + "/athletes/" + athlete[0].id;
        return athlete;
      }
    });
}

function get_athlete_from_sub(athlete_sub, req) {
  var q = datastore.createQuery(ATHLETES);
  const results = {};
  return datastore.runQuery(q).then((entities) => {
    results.athletes = entities[0].map(fromDatastore).filter( item => item.sub_id === athlete_sub);
    for (var item of results.athletes) {
      item.self = req.protocol + "://" + req.get("host") + "/races/" + item.id;
    }
    return results.athletes[0];
  });
}

function get_athlete_ids() {
  var q = datastore.createQuery(ATHLETES);
  return datastore.runQuery(q).then((entities) => {
    const athletes = entities[0].map(fromDatastore);
    var ids = [];
    for (var athlete of athletes) {
      ids.push(athlete.sub_id);
    }
    return ids;
  });
}

function get_athletes(req) {
  var q = datastore.createQuery(ATHLETES).limit(5);
  var results = {};
  if(Object.keys(req.query).includes("cursor")){
    q = q.start(req.query.cursor);
  }
  return datastore.runQuery(q).then((entities) => {
    results.athletes = entities[0].map(fromDatastore);
    for (var item of results.athletes) {
      item.self = req.protocol + "://" + req.get("host") + "/athletes/" + item.id;
    }
    if(entities[1].moreResults !== datastore.NO_MORE_RESULTS ){
        results.next = req.protocol + "://" + req.get("host") + "/athletes" + "?cursor=" + entities[1].endCursor;
    }
    return results;
  });
}

/* ------------- End Athlete Model Functions ------------- */

/* ------------- Begin Race Model Functions ------------- */
function post_race(name, type, max_entries, creator_id) {
  var key = datastore.key(RACES);
  const data = { "name": name, "type": type, "max_entries": max_entries, "athletes" : [], "course": null, "creator_id": creator_id};
  return datastore.save({ "key": key, "data": data }).then(() => { return key });
}

function validate_race_input(body) {
  if (body.name) {
    if ((INVALID_CHARS.test(body.name)) || (body.name.length >= 2 * MAX_LEN)) {
      return false;
    }
  }
  if (body.type) {
    if ((INVALID_CHARS.test(body.type)) || (body.type.length >= MAX_LEN)) {
      return false;
    }
  }
  if (body.max_entries) {
    if ((parseInt(body.max_entries) < 0)) {
      return false;
    }
  }
  return true;
}

function patch_race(race_id, body) {
  const key = datastore.key([RACES, parseInt(race_id, 10)]);
  return datastore.get(key).then((entity) => {
    if (entity[0] === undefined || entity[0] === null) {
      return entity;
    } else {
      const old_race = entity.map(fromDatastore);
      var data = { "name": old_race[0].name, "type": old_race[0].type, "max_entries": old_race[0].max_entries, "course": old_race[0].course, "athletes": old_race[0].athletes, "creator_id": old_race[0].creator_id};
      if (body.name) {
        data.name = body.name;
      }
      if (body.type) {
        data.type = body.type;
      }
      if (body.max_entries) {
        data.max_entries = body.max_entries;
      }
      return datastore.save({ "key": key, "data": data }).then(() => { return key });
    }
  });
}

function put_race(race_id, name, type, max_entries) {
  var key = datastore.key([RACES, parseInt(race_id, 10)]);
  return datastore.get(key).then((entity) => {
    if (entity[0] === undefined || entity[0] === null) {
      return entity;
    } else {
      const old_race = entity.map(fromDatastore);
      const data = { "name": name, "type": type, "max_entries": max_entries, "course": old_race[0].course, "athletes": old_race[0].athletes, "creator_id": old_race[0].creator_id};
      return datastore.save({ "key": key, "data": data }).then(() => { return key });
    }
  });
}

function get_races(creator_id, req) {
  var q = datastore.createQuery(RACES).limit(5);
  const results = {};
  if(Object.keys(req.query).includes("cursor")){
    q = q.start(req.query.cursor);
  }
  return datastore.runQuery(q).then((entities) => {
    results.races = entities[0].map(fromDatastore).filter( item => item.creator_id === creator_id);
    for (var item of results.races) {
      item.self = req.protocol + "://" + req.get("host") + "/races/" + item.id;
    }
    if(entities[1].moreResults !== datastore.NO_MORE_RESULTS ){
        results.next = req.protocol + "://" + req.get("host") + "/races" + "?cursor=" + entities[1].endCursor;
    }
    return results;
  });
}

function get_race(race_id, req) {
  const key = datastore.key([RACES, parseInt(race_id, 10)]);
    return datastore.get(key).then((entity) => {
      if (entity[0] === undefined || entity[0] === null) {
        return entity;
      } else {
        var race = entity.map(fromDatastore);
        race[0].self = req.protocol + "://" + req.get("host") + "/races/" + race[0].id;
        return race;
      }
    });
}

function delete_race(race_id) {
  const key = datastore.key([RACES, parseInt(race_id, 10)]);
  return datastore.get(key).then((entity) => {
    const race = entity.map(fromDatastore);
    if (race[0].course != null) {
      delete_course_race(race[0].course.id, race_id).then(() => {
        const promises = [];
        for (var athlete of race[0].athletes) {
          promises.push(delete_athlete_race(race_id, athlete.id));
        }
        Promise.all(promises).then(() => {
          return datastore.delete(key).then((key) => { return key });
        });
      });
    } else {
      return datastore.delete(key).then((key) => { return key });
    }
  });
}

app.patch('/races', function (req, res) {
  res.status(405).json({ 'Error': 'PATCH /races not allowed.'});
});

app.put('/races', function (req, res) {
  res.status(405).json({ 'Error': 'PUT /races not allowed.'});
});

app.delete('/races', function (req, res) {
  res.status(405).json({ 'Error': 'DELETE /races not allowed.'});
});
/* ------------- End Race Model Functions ------------- */

/* ------------- Begin Course Model Functions ------------- */
function post_course(name, distance, city, state) {
  var key = datastore.key(COURSES);
  const data = { "name": name, "distance": distance, "city": city, "state": state, "races" : []};
  return datastore.save({ "key": key, "data": data }).then(() => { return key });
}

function validate_course_input(body) {
  if (body.name) {
    if ((INVALID_CHARS.test(body.name)) || (body.name.length >= 2 * MAX_LEN)) {
      return false;
    }
  }
  if (body.city) {
    if ((INVALID_CHARS.test(body.city)) || (body.city.length >= MAX_LEN)) {
      return false;
    }
  }
  if (body.state) {
    if ((INVALID_CHARS.test(body.state)) || (body.state.length > 2)) {
      return false;
    }
  }
  if (body.distance) {
    if ((parseInt(body.distance) < 0)) {
      return false;
    }
  }
  return true;
}

function patch_course(course_id, body) {
  const key = datastore.key([COURSES, parseInt(course_id, 10)]);
  return datastore.get(key).then((entity) => {
    if (entity[0] === undefined || entity[0] === null) {
      return entity;
    } else {
      const old_course = entity.map(fromDatastore);
      var data = { "name": old_course[0].name, "distance": old_course[0].distance, "city": old_course[0].city, "state": old_course[0].state, "races": old_course[0].races};
      if (body.name) {
        data.name = body.name;
      }
      if (body.distance) {
        data.distance = body.distance;
      }
      if (body.city) {
        data.city = body.city;
      }
      if (body.state) {
        data.state = body.state;
      }
      return datastore.save({ "key": key, "data": data }).then(() => { return key });
    }
  });
}

function put_course(course_id, name, distance, city, state) {
  var key = datastore.key([COURSES, parseInt(course_id, 10)]);
  return datastore.get(key).then((entity) => {
    if (entity[0] === undefined || entity[0] === null) {
      return entity;
    } else {
      const old_course = entity.map(fromDatastore);
      const data = { "name": name, "distance": distance, "city": city, "state": state, "races": old_course[0].races};
      return datastore.save({ "key": key, "data": data }).then(() => { return key });
    }
  });
}

function get_courses(req) {
  var q = datastore.createQuery(COURSES).limit(5);;
  const results = {};
  if(Object.keys(req.query).includes("cursor")){
    q = q.start(req.query.cursor);
  }
  return datastore.runQuery(q).then((entities) => {
    results.courses = entities[0].map(fromDatastore);
    for (var item of results.courses) {
      item.self = req.protocol + "://" + req.get("host") + "/courses/" + item.id;
    }
    if(entities[1].moreResults !== datastore.NO_MORE_RESULTS ){
        results.next = req.protocol + "://" + req.get("host") + "/courses" + "?cursor=" + entities[1].endCursor;
    }
    return results;
  });
}

function get_course(course_id, req) {
  const key = datastore.key([COURSES, parseInt(course_id, 10)]);
    return datastore.get(key).then((entity) => {
      if (entity[0] === undefined || entity[0] === null) {
        return entity;
      } else {
        var course = entity.map(fromDatastore);
        course[0].self = req.protocol + "://" + req.get("host") + "/courses/" + course[0].id;
        return course;
      }
    });
}

function delete_course(course_id) {
  const key = datastore.key([COURSES, parseInt(course_id, 10)]);
  return datastore.get(key).then((entity) => {
    const course = entity.map(fromDatastore);
      const promises = [];
      for (var race of course[0].races) {
        promises.push(delete_race_course(course_id, race.id));
      }
      Promise.all(promises).then(() => {
        return datastore.delete(key).then((key) => { return key });
      });
  });
}
/* ------------- End Course Model Functions ------------- */

/* ------------- Begin Relationship Model Functions ------------- */
function put_course_race(course_id, race_id, req) {
  const key = datastore.key([COURSES, parseInt(course_id, 10)]);
  return datastore.get(key).then((entity) => {
    const course = entity.map(fromDatastore);
    const race = {"id": race_id, "self": req.protocol + "://" + req.get("host") + "/races/" + race_id};
    course[0].races.push(race);
    return datastore.save({"key":key, "data":course[0]});
  });
}

function put_race_course(course_id, race_id, req) {
  const key = datastore.key([RACES, parseInt(race_id, 10)]);
  return datastore.get(key).then((entity) => {
    const race = entity.map(fromDatastore);
    const course = {"id": course_id, "self": req.protocol + "://" + req.get("host") + "/courses/" + course_id};
    race[0].course = course;
    return datastore.save({"key":key, "data":race[0]});
  });
}

function delete_course_race(course_id, race_id) {
  const key = datastore.key([COURSES, parseInt(course_id, 10)]);
  return datastore.get(key).then((entity) => {
    const course = entity.map(fromDatastore);
    for (var race of course[0].races) {
      if (race.id == race_id) {
        course[0].races.pop(race);
      }
    }
    return datastore.save({"key":key, "data":course[0]});
  });
}

function delete_race_course(course_id, race_id) {
  const key = datastore.key([RACES, parseInt(race_id, 10)]);
  return datastore.get(key).then((entity) => {
    const race = entity.map(fromDatastore);
    race[0].course = null;
    return datastore.save({"key":key, "data":race[0]});
  });
}

function put_race_athlete(race_id, athlete_id, req) {
  const key = datastore.key([RACES, parseInt(race_id, 10)]);
  return datastore.get(key).then((entity) => {
    const race = entity.map(fromDatastore);
    const athlete = {"id": athlete_id, "self": req.protocol + "://" + req.get("host") + "/athletes/" + athlete_id};
    race[0].athletes.push(athlete);
    return datastore.save({"key":key, "data":race[0]});
  });
}

function put_athlete_race(race_id, athlete_id, req) {
  const key = datastore.key([ATHLETES, parseInt(athlete_id, 10)]);
  return datastore.get(key).then((entity) => {
    const athlete = entity.map(fromDatastore);
    const race = {"id": race_id, "self": req.protocol + "://" + req.get("host") + "/races/" + race_id};
    athlete[0].races.push(race);
    return datastore.save({"key":key, "data":athlete[0]});
  });
}

function delete_race_athlete(race_id, athlete_id) {
  const key = datastore.key([RACES, parseInt(race_id, 10)]);
  return datastore.get(key).then((entity) => {
    const race = entity.map(fromDatastore);
    for (var athlete of race[0].athletes) {
      if (athlete.id == athlete_id) {
        race[0].athletes.pop(athlete);
      }
    }
    return datastore.save({"key":key, "data":race[0]});
  });
}

function delete_athlete_race(race_id, athlete_id) {
  const key = datastore.key([ATHLETES, parseInt(athlete_id, 10)]);
  return datastore.get(key).then((entity) => {
    const athlete = entity.map(fromDatastore);
    for (var race of athlete[0].races) {
      if (race.id == race_id) {
        athlete[0].races.pop(race);
      }
    }
    return datastore.save({"key":key, "data":athlete[0]});
  });
}
/* ------------- End Relationship Model Functions ------------- */

/* ------------- Begin Relationship Controller Functions ------------- */
router.put('/courses/:course_id/races/:race_id', function (req, res) {
  const course = get_course(req.params.course_id, req)
  .then((course) => {
    const race = get_race(req.params.race_id, req)
      .then((race) => {
        if (course[0] === undefined || course[0] === null || race[0] === undefined || race[0] === null) {
          res.status(404).json({ 'Error': "The specified course and/or race does not exist"});
        } else if (race[0].course != null) {
            res.status(403).json({ 'Error': "The race is already assigned to another course" });
        } else {
          put_course_race(req.params.course_id, req.params.race_id, req).then(() => {
            put_race_course(req.params.course_id, req.params.race_id, req).then(() => {
              res.status(204).end();
          }); 
        }); 
      }
    });
  });
});

router.delete('/courses/:course_id/races/:race_id', function (req, res) {
  const course = get_course(req.params.course_id, req)
  .then((course) => {
    const race = get_race(req.params.race_id, req)
      .then((race) => {
      if (course[0] === undefined || course[0] === null || race[0] === undefined || race[0] === null || race[0].course == null) {
        res.status(404).json({ 'Error': "No course with this course_id is assigned to this race with this race_id"});
      } else if (race[0].course.id != req.params.course_id) {
        res.status(404).json({ 'Error': "No course with this course_id is assigned to this race with this race_id"});
      } else {
        delete_course_race(req.params.course_id, req.params.race_id).then(() => {
          delete_race_course(req.params.course_id, req.params.race_id).then(() => {
            res.status(204).end();
          }); 
        }); 
      }
    });
  });
});

router.put('/races/:race_id/athletes/:athlete_id', checkJwt, function (req, res) {
  const race = get_race(req.params.race_id, req)
  .then((race) => {
    const athlete = get_athlete(req.params.athlete_id, req)
      .then((athlete) => {
      if (race[0] === undefined || race[0] === null || athlete[0] === undefined || athlete[0] === null) {
        res.status(404).json({ 'Error': "The specified race and/or athlete does not exist"});
      } else {
        var already_entered = false;
        for (var ath_race of athlete[0].races) {
          if (ath_race.id == req.params.race_id) {
            already_entered = true;
          }
        }
        if (already_entered) {
          res.status(403).json({ 'Error': "The athlete is already entered in this race"});
        } else {
          put_race_athlete(req.params.race_id, req.params.athlete_id, req).then(() => {
            put_athlete_race(req.params.race_id, req.params.athlete_id, req).then(() => {
              res.status(204).end();
            }); 
          }); 
        }
      }
    });
  });
});

router.delete('/races/:race_id/athletes/:athlete_id', checkJwt, function (req, res) {
  const race = get_race(req.params.race_id, req)
  .then((race) => {
    const athlete = get_athlete(req.params.athlete_id, req)
      .then((athlete) => {
        if (race[0] === undefined || race[0] === null || athlete[0] === undefined || athlete[0] === null) {
          res.status(404).json({ 'Error': "No race with this race_id is assigned to this athlete with this athlete_id"});
        } else {
          var valid = false;
          for (var ath_race of athlete[0].races) {
            if (ath_race.id == req.params.race_id)
              valid = true
          }
          if (!valid) {
            res.status(404).json({ 'Error': "No race with this race_id is assigned to this athlete with this athlete_id"});
          } else {
            delete_race_athlete(req.params.race_id, req.params.athlete_id).then(() => {
              delete_athlete_race(req.params.race_id, req.params.athlete_id).then(() => {
                res.status(204).end();
              }); 
            }); 
          }
        }
    });
  });
});

/* ------------- End Relationship Controller Functions ------------- */

/* ------------- Begin Course Controller Functions ------------- */
router.post('/courses', function (req, res) {
  const accepts = req.accepts(['application/json']);
  if (!accepts){
    res.status(406).json({'Error': 'Server only sends application/json data.'});
  } else if (!req.body.name ||!req.body.distance || !req.body.city || !req.body.state) {
    res.status(400).json({ "Error": "The request object is missing at least one of the required attributes." });
  } else if (!validate_course_input(req.body)) {
    res.status(403).json({ 'Error': 'Request contains at least one invalid input.'});
  } else if (accepts === 'application/json'){
    post_course(req.body.name, req.body.distance, req.body.city, req.body.state)
    .then((key) => { 
      get_course(key.id, req)
      .then((course) => {
        res.status(201).json(course[0]);
      });
    }); 
  }
});

router.get('/courses/:course_id', function (req, res) {
  const course = get_course(req.params.course_id, req)
    .then((course) => {
      const accepts = req.accepts(['application/json']);
      if (course[0] === undefined || course[0] === null) {
        res.status(404).json({'Error': 'No course with this course_id exists.'});
      } else if(!accepts){
        res.status(406).json({'Error': 'Server only sends application/json data.'});
      } else if(accepts === 'application/json'){
        res.status(200).json(course[0]);
      } else { res.status(500).json({'Error': 'Server error getting course'}); }
    });
});

router.get('/courses', function (req, res) {
  const courses = get_courses(req)
    .then((courses) => {
      const accepts = req.accepts(['application/json']);
      if(!accepts){
        res.status(406).json({'Error': 'Server only sends application/json data.'});
      } else if(accepts === 'application/json'){
        res.status(200).json(courses);
      } else { res.status(500).json({'Error': 'Server error getting courses'}); }
    });
});

router.patch('/courses/:course_id', function (req, res) {
  const course = get_course(req.params.course_id, req)
  .then((course) => {
    const accepts = req.accepts(['application/json']);
    if (course[0] === undefined || course[0] === null) {
      res.status(404).json({ 'Error': 'No course with this course_id exists.' });
    } else if (!accepts){
      res.status(406).json({'Error': 'Server only sends application/json data.'});
    } else if (!validate_course_input(req.body)) {
      res.status(403).json({ 'Error': 'Request contains at least one invalid input.'});
    } else if (accepts === 'application/json'){
      patch_course(req.params.course_id, req.body)
      .then((key) => { 
        get_course(key.id, req)
        .then((course) => {
          res.status(200).json(course[0]);
        });
      }); 
    }
  });
});

router.put('/courses/:course_id', function (req, res) {
  const course = get_course(req.params.course_id, req)
  .then((course) => {
    if (course[0] === undefined || course[0] === null) {
      res.status(404).json({ 'Error': 'No course with this course_id exists.'});
    } else if (!req.body.name ||!req.body.distance || !req.body.city || !req.body.state) {
      res.status(400).json({ "Error": "The request object is missing at least one of the required attributes." });
    } else {
      const accepts = req.accepts(['application/json']);
      if (!accepts){
        res.status(406).json({'Error': 'Server only sends application/json data.'});
      } else if (!validate_course_input(req.body)) {
        res.status(403).json({ 'Error': 'Request contains at least one invalid input.'});
      } else if (accepts === 'application/json'){
        put_course(req.params.course_id, req.body.name, req.body.distance, req.body.city, req.body.state)
        .then((key) => { 
          get_course(key.id, req)
          .then((course) => {
            res.status(200).json(course[0]);
          });
        }); 
      }
    }
  });
});

app.delete('/courses/:course_id', function (req, res) {
  const course = get_course(req.params.course_id, req)
    .then((course) => {
      if (course[0] === undefined || course[0] === null) {
        res.status(404).json({ 'Error': 'No course with this course_id exists.' });
      } else {
        delete_course(req.params.course_id).then( () => {
          res.status(204).end();
        });
      }
    });
});

app.patch('/courses', function (req, res) {
  res.status(405).json({ 'Error': 'PATCH /courses not allowed.'});
});

app.put('/courses', function (req, res) {
  res.status(405).json({ 'Error': 'PUT /courses not allowed.'});
});

app.delete('/courses', function (req, res) {
  res.status(405).json({ 'Error': 'DELETE /courses not allowed.'});
});
/* ------------- End Course Controller Functions ------------- */

/* ------------- Begin Race Controller Functions ------------- */
router.post('/races', checkJwt, function (req, res) {
  const accepts = req.accepts(['application/json']);
  if (!accepts){
    res.status(406).json({'Error': 'Server only sends application/json data.'});
  } else if (!req.body.name ||!req.body.type || !req.body.max_entries) {
    res.status(400).json({ "Error": "The request object is missing at least one of the required attributes." });
  } else if (!validate_race_input(req.body)) {
    res.status(403).json({ 'Error': 'Request contains at least one invalid input.'});
  } else if (accepts === 'application/json'){
    post_race(req.body.name, req.body.type, req.body.max_entries, req.user.sub)
    .then((key) => { 
      get_race(key.id, req)
      .then((race) => {
        res.status(201).json(race[0]);
      });
    }); 
  }
});

router.get('/races/:race_id', checkJwt,function (req, res) {
  const race = get_race(req.params.race_id, req)
    .then((race) => {
      const accepts = req.accepts(['application/json']);
      if (race[0] === undefined || race[0] === null) {
        res.status(404).json({ 'Error': 'No race with this race_id exists.'});
      } else if (race[0].creator_id != req.user.sub) {
        res.status(403).json({ 'Error': "You are not authorized to view the race with this race_id."});
      } else if(!accepts){
        res.status(406).json({'Error': 'Server only sends application/json data.'});
      } else if(accepts === 'application/json'){
        res.status(200).json(race[0]);
      } else { res.status(500).json({'Error': 'Server error getting race'}); }
    });
});

router.get('/races', checkJwt, function (req, res) {
  const races = get_races(req.user.sub, req)
    .then((races) => {
      const accepts = req.accepts(['application/json']);
      if(!accepts){
        res.status(406).json({'Error': 'Server only sends application/json data.'});
      } else if(accepts === 'application/json'){
        res.status(200).json(races);
      } else { res.status(500).json({'Error': 'Server error getting races'}); }
    });
});

router.patch('/races/:race_id', checkJwt, function (req, res) {
  const race = get_race(req.params.race_id, req)
  .then((race) => {
    const accepts = req.accepts(['application/json']);
    if (race[0] === undefined || race[0] === null) {
      res.status(404).json({ 'Error': 'No race with this race_id exists.' });
    } else if (race[0].creator_id != req.user.sub) {
      res.status(403).json({ 'Error': "You are not authorized to edit the race with this race_id."});
    } else if (!accepts){
      res.status(406).json({'Error': 'Server only sends application/json data.'});
    } else if (!validate_race_input(req.body)) {
      res.status(403).json({ 'Error': 'Request contains at least one invalid input.'});
    } else if (accepts === 'application/json'){
      patch_race(req.params.race_id, req.body)
      .then((key) => { 
        get_race(key.id, req)
        .then((race) => {
          res.status(200).json(race[0]);
        });
      }); 
    }
  });
});

router.put('/races/:race_id', checkJwt, function (req, res) {
  const race = get_race(req.params.race_id, req)
  .then((race) => {
    if (!req.body.name ||!req.body.type || !req.body.max_entries) {
      res.status(400).json({ "Error": "The request object is missing at least one of the required attributes." });
    } else if (race[0] === undefined || race[0] === null) {
      res.status(404).json({ 'Error': 'No race with this race_id exists.' });
    } else if (race[0].creator_id != req.user.sub) {
      res.status(403).json({ 'Error': "You are not authorized to edit the race with this race_id."});
    } else {
      const accepts = req.accepts(['application/json']);
      if (!accepts){
        res.status(406).json({'Error': 'Server only sends application/json data.'});
      } else if (!validate_race_input(req.body)) {
        res.status(403).json({ 'Error': 'Request contains at least one invalid input.'});
      } else if (accepts === 'application/json'){
        put_race(req.params.race_id, req.body.name, req.body.type, req.body.max_entries)
        .then((key) => { 
          get_race(key.id, req)
          .then((race) => {
            res.status(200).json(race[0]);
          });
        }); 
      }
    }
  });
});

app.delete('/races/:race_id', checkJwt, function (req, res) {
  const race = get_race(req.params.race_id, req)
    .then((race) => {
      if (race[0] === undefined || race[0] === null) {
        res.status(404).json({ 'Error': 'No race with this race_id exists.' });
      } else if (race[0].creator_id != req.user.sub) {
        res.status(403).json({'Error': "You are not authorized to edit the race with this race_id."});
      } else {
        delete_race(req.params.race_id).then( () => {
          res.status(204).end();
        });
      }
    });
});
/* ------------- End Race Controller Functions ------------- */

/* ------------- Begin Athlete Controller Functions ------------- */
router.post('/athletes', function (req, res) {
  const accepts = req.accepts(['application/json']);
  if (!accepts){
    res.status(406).json({'Error': 'Server only sends application/json data.'});
  } else if (accepts === 'application/json'){
    get_athlete_ids().then((ids) => {
      if (ids.includes(req.body.sub)) {
        get_athlete_from_sub(req.body.sub, req)
          .then((athlete) => {
            res.status(201).json(athlete);
          });
      } else {
        post_athlete(req.body.sub)
        .then((key) => { 
          get_athlete(key.id, req)
          .then((athlete) => {
            res.status(201).json(athlete[0]);
          });
        }); 
      }
    });
  }
});

router.patch('/athletes/:athlete_id', checkJwt, function (req, res) {
  const athlete = get_athlete(req.params.athlete_id, req)
  .then((athlete) => {
    if (athlete[0] === undefined || athlete[0] === null) {
      res.status(404).json({ 'Error': 'No athlete with this athlete_id exists.' });
    } else if (athlete[0].sub_id != req.user.sub) {
      res.status(403).json({'Error': "You are not authorized to edit the athlete with this athlete_id."});
    } else {
      const accepts = req.accepts(['application/json']);
      if (!accepts){
        res.status(406).json({'Error': 'Server only sends application/json data.'});
      } else if (accepts === 'application/json'){
        patch_athlete(req.params.athlete_id, req.body)
        .then((key) => { 
          get_athlete(key.id, req)
          .then((athlete) => {
            res.status(200).json(athlete[0]);
          });
        }); 
      }
    }
  });
});

router.get('/athletes/:athlete_id', checkJwt, function (req, res) {
  const athlete = get_athlete(req.params.athlete_id, req)
    .then((athlete) => {
      const accepts = req.accepts(['application/json']);
      if (athlete[0] === undefined || athlete[0] === null) {
        res.status(404).json({ 'Error': 'No athlete with this athlete_id exists.' });
      } else if (athlete[0].sub_id != req.user.sub) {
        res.status(403).json({'Error': "You are not authorized to view the athlete with this athlete_id."});
      } else if(!accepts){
        res.status(406).json({'Error': 'Server only sends application/json data.'});
      } else if(accepts === 'application/json'){
        res.status(200).json(athlete[0]);
      } else { res.status(500).json({'Error': 'Server error getting athlete'}); }
    });
});

router.get('/athletes', function (req, res) {
  const athletes = get_athletes(req)
    .then((athletes) => {
      const accepts = req.accepts(['application/json']);
      if(!accepts){
        res.status(406).json({'Error': 'Server only sends application/json data.'});
      } else if(accepts === 'application/json'){
        res.status(200).json(athletes);
      } else { res.status(500).json({'Error': 'Server error getting athletes'}); }
    });
});

app.patch('/athletes', function (req, res) {
  res.status(405).json({ 'Error': 'PATCH /athletes not allowed.'});
});

app.put('/athletes', function (req, res) {
  res.status(405).json({ 'Error': 'PUT /athletes not allowed.'});
});

app.delete('/athletes', function (req, res) {
  res.status(405).json({ 'Error': 'DELETE /athletes not allowed.'});
});

/* ------------- End Athlete Controller Functions ------------- */

login.post('/', function(req, res){
  const username = req.body.username;
  const password = req.body.password;
  var options = { method: 'POST',
          url: `https://${DOMAIN}/oauth/token`,
          headers: { 'content-type': 'application/json' },
          body:
           { grant_type: 'password',
             username: username,
             password: password,
             client_id: CLIENT_ID,
             client_secret: CLIENT_SECRET },
          json: true };
  request(options, (error, response, body) => {
      if (error){
        res.status(500).send(error);
      } else {
        res.send(body);
      }
  });
});

app.use('', router);
app.use('/login', login);

app.use(function (err, req, res, next) {
  if (err.name === "UnauthorizedError") {
    res.status(401).json({"Error" : "User is not authenticated. Please log in."});
  } else {
    next(err);
  }
});

// Listen to the App Engine-specified port, or 8080 otherwise
const PORT = process.env.PORT || 8080;
app.listen(PORT, () => {
  console.log(`Server listening on port ${PORT}...`);
});