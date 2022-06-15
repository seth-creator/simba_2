function populate() {
    var today = new Date();
    var theDate = new Date(document.forms["vars"]["getDateVar"].value);
    var month = theDate.getMonth();

    var weekday = getFirstWeekDay(theDate);

    var year = 0;

    year = theDate.getYear() - 100 + 2000;

    setDatePickerYear(year);

    setDatePickerMonth(month);


    var lastDay;
    today.setFullYear(year, month, 1);

    for (var i = 1; i < 43 ; i++) {
        document.getElementById("dayA" + i).innerText = "";
        document.getElementById("daysCell" + i).className = "daysCell";
    }

    for (i = weekday; i < 60 ; i++) {
        document.getElementById("dayA" + i).innerText = (i - weekday + 1);

        lastDay = today.getDate();

        today.setDate(today.getDate() + 1);

        if (month != today.getMonth())
            break;
    }

    setDayClass(weekday, lastDay);
    if (document.forms["vars"]["pickedDateVar"].value != "") checkPickedDate();

}

function getFirstWeekDay(theDate) {
    var theDate1 = new Date(theDate);

    var weekday;

    theDate1.setDate(1);

    weekday = theDate1.getDay();

    weekday++;
    if (weekday == 8) weekday = 1;
    return weekday;
}

function setDayClass(weekday, lastDay) {
    var today = new Date();
    var checkDate = new Date();
    var theDate = new Date(document.forms["vars"]["getDateVar"].value);
    var month = theDate.getMonth();

    var year = 0;
    var day;

    year = theDate.getYear() - 100 + 2000;


    for (var i = 1 ; i < 43 ; i++) {
        day = document.getElementById("dayA" + i).innerText;

        if (day != "") {

            checkDate.setFullYear(year, month, day);


            if (checkDate >= today) {
                document.getElementById("dayA" + i).className = "dayA";
            }
            else {
                document.getElementById("dayA" + i).className = "dayANoLink";
            }
        }

    }


}

function openDatePicker() {

    document.getElementById("datePickerMainDiv").style.display = "block";

    var today = new Date();

    if (document.forms["vars"]["pickedDateVar"].value == "") {
        document.forms["vars"]["getDateVar"].value = today;
    }
    else {
        document.forms["vars"]["getDateVar"].value = document.forms["vars"]["pickedDateVar"].value;
    }


    populate();

    document.getElementById("testDate").disabled = true;
    document.getElementById("testDate").style.backgroundColor = "#fff";
    //document.getElementById("datePickerMainDiv").focus();

}

function closeDatePicker() {
    document.getElementById("datePickerMainDiv").style.display = "none";
    document.getElementById("testDate").disabled = false;

    document.getElementById("testDate").focus();
}

function setDateText() {
    if (document.forms["vars"]["pickedDateVar"].value != "") {

        var pickedDate = new Date(document.forms["vars"]["pickedDateVar"].value);

        var yearStr = String(pickedDate.getYear() + 2000 - 100);

        var monthStr = String(pickedDate.getMonth() + 1);

        if (monthStr.length == 1)
            monthStr = "0" + monthStr;
        var dayStr = String(pickedDate.getDate());
        if (dayStr.length == 1)
            dayStr = "0" + dayStr;
        var dateText = dayStr + "/" + monthStr + "/" + yearStr;

        document.forms["testForm"]["testDate"].value = dateText;
    }
}


function setDatePickerYear(year) {
    document.getElementById("datePickerYear").innerText = year;
}

function setDatePickerMonth(month) {

    var monthText = "";

    switch (month) {
        case 0: monthText = "ינואר"; break;
        case 1: monthText = "פברואר"; break;
        case 2: monthText = "מרץ"; break;
        case 3: monthText = "אפריל"; break;
        case 4: monthText = "מאי"; break;
        case 5: monthText = "יוני"; break;
        case 6: monthText = "יולי"; break;
        case 7: monthText = "אוגוסט"; break;
        case 8: monthText = "ספטמבר"; break;
        case 9: monthText = "אוקטובר"; break;
        case 10: monthText = "נובמבר"; break;
        case 11: monthText = "דצמבר"; break;

    }

    document.getElementById("datePickerMonth").innerText = monthText;
}

function pickDate(aNum) {

    var theDay = document.getElementById("dayA" + aNum).innerText;

    var theDate = new Date(document.forms["vars"]["getDateVar"].value);

    var month = theDate.getMonth();

    var year = theDate.getYear() - 100 + 2000;

    var pickedDate = new Date();

    pickedDate.setFullYear(year, month, theDay);

    document.forms["vars"]["pickedDateVar"].value = pickedDate;
    //document.forms["vars"]["pickedA"].value = aNum;

    document.getElementById("daysCell" + aNum).className = "pickedCell";

    checkPickedDate();
    setDateText();


}


function nextMonth() {
    var theDate = new Date(document.forms["vars"]["getDateVar"].value);

    var month = theDate.getMonth();

    var year = 0;

    year = theDate.getYear() - 100 + 2000;

    month++;
    if (month == 12) {
        month = 0;
        year++;
    }

    theDate.setFullYear(year, month, 1);
    document.forms["vars"]["getDateVar"].value = theDate;
    populate();

}

function prevMonth() {
    var theDate = new Date(document.forms["vars"]["getDateVar"].value);

    var month = theDate.getMonth();

    var year = 0;

    year = theDate.getYear() - 100 + 2000;

    month--;
    if (month == -1) {
        month = 11;
        year--;
    }

    theDate.setFullYear(year, month, 1);
    document.forms["vars"]["getDateVar"].value = theDate;
    populate();
}

function checkPickedDate() {
    var theDate = new Date(document.forms["vars"]["getDateVar"].value);
    var theDateStr = String(theDate.getFullYear()) + String(theDate.getMonth()) + String(theDate.getDate());

    var pickedDate = new Date(document.forms["vars"]["pickedDateVar"].value);
    var pickedDateStr = String(pickedDate.getFullYear()) + String(pickedDate.getMonth()) + String(pickedDate.getDate());

    for (var i = 1 ; i < 43 ; i++) {
        if (document.getElementById("dayA" + i).innerText != "") {

            theDate.setDate(document.getElementById("dayA" + i).innerText);
            theDateStr = String(theDate.getFullYear()) + String(theDate.getMonth()) + String(theDate.getDate());

            if (theDateStr != pickedDateStr) {
                document.getElementById("daysCell" + i).className = "daysCell";
            }
            else {
                document.getElementById("daysCell" + i).className = "pickedCell";
            }
        }
    }
}