/*
    A simple function to show a notification at the top of the page.

    @param title the title of the notification
    @param message the notification message
    @param type the type of notification
    @param where the ID of the parent
 */

function showNotification(title, message, type, where)
{
    var notificationEl = document.getElementById(where),
        theNotification = document.createElement('div'),
        notificationTitle = document.createElement('strong'),
        notificationMessage = document.createTextNode(message);

    notificationTitle.innerHTML = title + " ";

    theNotification.setAttribute('class', 'alert ' + type + ' duchemin-notify');
    theNotification.setAttribute('style', 'margin-bottom:0;');
    theNotification.setAttribute('role', 'alert');

    theNotification.appendChild(notificationTitle);
    theNotification.appendChild(notificationMessage);

    notificationEl.appendChild(theNotification);

    // after 5 seconds fade out the notification
    window.setTimeout(function ()
    {
        $(theNotification).fadeTo(500, 0).slideUp(500, function ()
        {
            $(this).remove();
        })
    }, 5000);
}