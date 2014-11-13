/*
    A simple function to show a notification at the top of the page.
 */

function showNotification(title, message, type)
{
    var notificationEl = document.getElementById("notifications"),
        theNotification = document.createElement('div');

    theNotification.setAttribute('class', 'alert alert-success');
    theNotification.innerHTML = message;

    notificationEl.appendChild(theNotification);
}