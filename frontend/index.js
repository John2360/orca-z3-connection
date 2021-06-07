function getContent()
{
    return document.getElementById("text-area").value;
}

$(document).ready(() =>
{
    $("#send-button").on('click', () =>
    {
        $.ajax({
            type : 'post',
            url : 'http://127.0.0.1:5000/checker',
            data : getContent,
            success : ()  => 
            {
                console.log('request sent')
            }
        });
    });
});