/*
Author: Corneel den Hartogh
Course: Heuristics

Description: Handle (loading and showing data) all user-input

*/

$.getJSON("visual.json", function(json) {
  
  // set variables
  var table = document.getElementById("table");
  var tableBody = document.createElement('tbody');
  table.appendChild(tableBody);
  var rosters = json
  var classrooms = json[0].roster.classrooms;
  var subjects = json[0].roster.subjects;
  var students = json[0].roster.students;
  var activities = json[0].roster.activities;
  var issues = json[0].roster.issues;
  // give default values for timetable selection
  var rosterIndex = 0;
  var objectIndex = 0;
  var selection = "classrooms";

  // setting the dropdown menu's
  $(rosters).each(function (index) {    
      var $option = $("<option/>").attr("value", index).text("Roster: " + rosters[index].name);
      $('#rosters').append($option);
  });
  $(classrooms).each(function (index) {    
      var $option = $("<option/>").attr("value", index).text(classrooms[index].number);
      $('#classrooms').append($option);
  });
  $(subjects).each(function (index) {    
      var $option = $("<option/>").attr("value", index).text(subjects[index].subject);
      $('#subjects').append($option);
  });
  $(students).each(function (index) {    
      var $option = $("<option/>").attr("value", index).text(students[index].student);
      $('#students').append($option);
  });
  $(issues).each(function (index) {    
      var $option = $("<option/>").attr("value", index).text(issues[index].category  + ": " + issues[index].reference);
      $('#issues').append($option);
  });
  // change functions for dropdown menu's
  $("#rosters").change(function() {
    index = $(this).find("option:selected").attr('value')
    remove();
    update(index, selection, objectIndex);
  });
  $("#classrooms").change(function() {
    index = $(this).find("option:selected").attr('value')
    remove();
    update(rosterIndex, "classrooms", index);
  });
  $("#subjects").change(function() {
    index = $(this).find("option:selected").attr('value')
    remove();
    update(rosterIndex, "subjects", index);
  });
  $("#students").change(function() {
    index = $(this).find("option:selected").attr('value')
    remove();
    update(rosterIndex,"students", index);
  });
  $("#issues").change(function() {
    index = $(this).find("option:selected").attr('value')
    category = issues[index].category
    reference = issues[index].reference
    findIssue(rosterIndex,index, category, reference);
  });
  $("#studentList").change(function() {
    index = $(this).find("option:selected").attr('value')
    remove();
    update(rosterIndex,"students", index);
  });
  // make the slots clickable in order to show students in activities
  $("#table").on('click', 'td', function() {
    var studentList = document.getElementById("studentList");
    for (var j = studentList.length -1; j >= 0; --j) {
      if(studentList[j].value != "") {
        studentList.remove(j);      
      }
    }

    var activityStudents = $(this).find("p").html();
    if (activityStudents != undefined) {
      var activityList = activityStudents.split(",");
      for (var i = 0; i < activityList.length; i++) {
        for (var j = 0; j < students.length; j++) {
          if(activityList[i] == students[j].student) {
            var $option = $("<option/>").attr("value", j).text(activityList[i]);
            $("#studentList").append($option);
          }
        }
      }
    }
  });
  
  update(rosterIndex,selection,objectIndex);

  // draw the selected timetable
  function update(rosterI, select,index) {

    selection = select;
    objectIndex = index
    rosterIndex = rosterI
    issues = json[rosterIndex].roster.issues;

    // thee issue list can differ
    $(issues).each(function (index) {    
        var $option = $("<option/>").attr("value", index).text(issues[index].category  + ": " + issues[index].reference);
        $('#issues').append($option);
    });

    var activities = []
    var value;

    if (selection === "classrooms") {
      value = json[rosterIndex].roster.classrooms[index].number;
      for (var i = 0; i < json[rosterIndex].roster.activities.length; i++) {
        if (index == json[rosterIndex].roster.activities[i].activity.slot[2]) {
          activities.push(json[rosterIndex].roster.activities[i].activity)
        }
      }
    }

    else if (selection === "students") {
      value = json[rosterIndex].roster.students[index].student.slice(-8);
      for (var i = 0; i < json[rosterIndex].roster.activities.length; i++) {
        for (var j = 0; j <json[rosterIndex].roster.activities[i].activity.students.length; j++) {
          if (json[rosterIndex].roster.students[index].student == json[rosterIndex].roster.activities[i].activity.students[j]) {
            activities.push(json[rosterIndex].roster.activities[i].activity);
          }
        }
      }
    }

    else if (selection === "subjects") {
      value = json[rosterIndex].roster.subjects[index].subject;
      if (value.length > 12) {
        value = value.slice(0,12) + "..."
      }
      for (var i = 0; i < json[rosterIndex].roster.activities.length; i++) {
        if (json[rosterIndex].roster.subjects[index].subject == json[rosterIndex].roster.activities[i].activity.subject) {
          activities.push(json[rosterIndex].roster.activities[i].activity);
        }      
      }
    }

    optimal = false;
    notOptimal = false;
    suboptimal = false;

    if (selection === "subjects") {
      suboptimal = subjectSpread(activities);
    }

    var range = [0,1,2,3,4];

    var week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"];
    var time = ["9.00 - 11.00", "11.00 - 13.00", "13.00 - 15.00", "15.00 - 17.00", "17.00 - 19.00"]

    var tableHeader = document.createElement('tr');
    tableBody.appendChild(tableHeader);
    var th = document.createElement('th');

    th.innerHTML = selection.slice(0,-1) + ":<br>" + value;
    tableHeader.appendChild(th);


    for (x in range) {
      var th = document.createElement('th');
      var day = document.createTextNode(week[x]);
      th.appendChild(day);
      tableHeader.appendChild(th)
    }

    for (x in range) {
      var tr = document.createElement('tr');
      tableBody.appendChild(tr);
      var td = document.createElement('td');
      var timeslot = document.createTextNode(time[x]);
      td.appendChild(timeslot);
      tr.appendChild(td);
      for (y in range) {
        var td = document.createElement('td');
        var slotActivities = 0;
        tr.appendChild(td);
        for (var i = 0; i < activities.length; i++) {
          if (JSON.stringify(activities[i].slot.slice(0,2)) == JSON.stringify([parseInt(y),parseInt(x)])) {
            td.innerHTML += "Subject: "+activities[i].subject + "<br> Kind: "+activities[i].kind+"<br> Lecture / Group nr: " +
            activities[i].lecture_number + " / " + activities[i].group +"<br> Amount Students: "+ 
            activities[i].amountStud+"<br> Room (cap): " + json[rosterIndex].roster.classrooms[activities[i].slot.slice(2)].number + 
            " (" + json[rosterIndex].roster.classrooms[activities[i].slot.slice(2)].capacity +")<br>" +
            "<p style='display: none'>" + activities[i].students + "</p>";
            slotActivities++;
            if (suboptimal === true) {
              td.style.background = 'lightsalmon';
            }
            else if (optimal === true) {
              td.style.background = 'lightgreen';
            }
            // selected a room, red means over capacity
            if (selection === "classrooms") {
              if (activities[i].amountStud > json[rosterIndex].roster.classrooms[activities[i].slot.slice(2)].capacity) {
                td.style.background = 'salmon';
              }
              else if (activities[i].slot[1] == 4 ) {
                td.style.background = 'lightsalmon';
              }
            }
            // selected students, red means more than 1 activity in one timeslot
            if (selection === "students" && slotActivities > 1) {
             td.style.background = 'salmon';
            }
            // selected subjects, red means more than 1 
            if (activities[i].red == "yes") {
             td.style.background = 'salmon';              
            }
          }
        }
      }
    }   
  }
  // find the object with issue in the knwon category
  function findIssue(rosterIndex, index, category, reference) {

    if (category == "Room") {
      for (var i = 0; i < json[rosterIndex].roster.classrooms.length; i++) {
        if (json[rosterIndex].roster.classrooms[i].number == reference) {
          remove();
          update(rosterIndex,"classrooms", i);
        }
      }
    }
    else if (category == "Stud.") {
      for (var i = 0; i < json[rosterIndex].roster.students.length; i++) {
        if (json[rosterIndex].roster.students[i].student == reference) {
          remove();
          update(rosterIndex, "students", i);
        }
      }
    }
    else if (category == "Subject") {
      for (var i = 0; i < json[rosterIndex].roster.subjects.length; i++) {
        if (json[rosterIndex].roster.subjects[i].subject == reference) {
          remove();
          update(rosterIndex, "subjects", i);
        }
      }
    }
  }

  // reset buttons and table
  function remove () {
    $("#table > tbody").html("");
    
    selectTags = document.getElementsByTagName("select");
    for (var i = 1; i < selectTags.length; i++) {
      selectTags[i].selectedIndex = 0;
    } 

    selectIssues = document.getElementById("issues");
    for (var j = selectIssues.length -1; j >= 0; --j) {
      if(selectIssues[j].value != "") {
        selectIssues.remove(j);      
      }
    }
  }

  // determine spread of subjects
  function subjectSpread (activities) {
    uniqueActivities = 0;
    days = []
    for (var i = 0; i < activities.length; i++) {
      days.push(activities[i].slot.slice(0,1))
      if (activities[i].kind == "Lecture" || activities[i].group == 0) {
        uniqueActivities ++;
      }
      for (var j = i+1; j < activities.length; j++) {
        if (JSON.stringify(activities[i].slot.slice(0,1)) == JSON.stringify(activities[j].slot.slice(0,1)) && 
          (activities[i].kind != activities[j].kind || activities[i].kind == "Lecture")) {
          activities[i].red = "yes";
          activities[j].red = "yes"
          notOptimal = true;
        }
      }
    }
    
    // with more than one activity, optimal spread is also possible
    if (notOptimal === false) {

      if (uniqueActivities == 2) {
        optimal = true;
        problem = false;
        for (var i = 0; i < days.length; i++) {
          if (days[i] != 0 && days[i] != 3) {
            problem = true;
            break;
          }
        }
        if (problem === true) {
          problem = false;
          for (var i = 0; i < days.length; i++) {
            if (days[i] != 1 && days[i] != 4) {
              problem = true;
              break;
            }
          }
          if (problem === true) {
            return true;
          }
        }
      }
      else if(uniqueActivities == 3) {
        optimal = true;
        for (var i = 0; i < days.length; i++) {
          if (days[i] == 1 || days[i] == 3) {
            return true;
          }
        }
      }
      else if (uniqueActivities == 4) {      
        optimal = true;
        for (var i = 0; i < days.length; i++) {
          if (days[i] == 2) {
            return true;
          }
        }        
      }
      else if (uniqueActivities == 5) {
        optimal = true;      
      }
    }
    return false;
  }
});