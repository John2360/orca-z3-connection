function getContent()
{
    return document.getElementById("text-area").value;
}

$(document).ready(() =>
{
    $("#checker-button").on('click', () =>
    {
        $.ajax({
            type : 'post',
            url : 'http://127.0.0.1:5000/checker',
            data : getContent,
            success : ()  => 
            {
                console.log('check request sent')
            }
        });
    });

    $("#simplify-button").on('click', () =>
    {
        $.ajax({
            type : 'post',
            url : 'http://127.0.0.1:5000/simplify',
            data : getContent,
            success : ()  => 
            {
                console.log('simplify request sent')
            }
        });
    });
});