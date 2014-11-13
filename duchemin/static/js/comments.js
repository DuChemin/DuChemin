var attachCommentAction = function ()
{
    $("#comment-submit").on("click", function (e)
    {
        e.preventDefault();
        var comment_text = $("#comment-field").val();

        if (!comment_text)
        {
            console.log("Empty text is not allowed!");
            // Handle errors here...
            return;
        }

        var piece_id = $(this).data('piece');

        var request = $.ajax({
            url: "/comments/",
            type: "POST",
            data: {
                'piece_id': piece_id,
                'comment_text': comment_text
            }
        });

        request.done(function(data, status, xhr)
        {
            console.log(status);

            var comment_div = document.createElement("div"),
                author_div = document.createElement("div"),
                header = document.createElement("h5"),
                author_link = document.createElement("a"),
                text_div = document.createElement("div"),
                text_para = document.createElement("p");

            comment_div.appendChild(author_div);
            comment_div.setAttribute('class', 'comment');

            author_div.appendChild(header);
            author_div.setAttribute('class', 'author');

            comment_div.appendChild(text_div);
            text_div.appendChild(text_para);
            text_div.setAttribute('class', 'text');

            author_link.setAttribute("href", data.author.profile.person.url);
            author_link.innerHTML = data.author.profile.person.full_name;

            var header_html = document.createTextNode(" (Just now)");
            header.appendChild(author_link);
            header.appendChild(header_html);

            text_para.innerHTML = data.text;

            var parent_element = document.getElementById("discussion-block");
            parent_element.insertBefore(comment_div, parent_element.firstChild);

            // clear the comment field.
            $("#comment-field").val("");

            showNotification("Success!", "Your comment was successfully added.", 'success');
        });

        return false;
    });
};
