function getContent()
{
    return document.getElementById("text-area").value;
}

$(document).ready(() =>
{
    $("#checker-button").on('click', () =>
    {
        $.ajax({
            type : 'POST',
            contentType: "application/json",
            url : 'http://127.0.0.1:5000/checker',
            data : getContent(),
            success : (data)  => 
            {
                console.log(data)
            }
        });
    });

    $("#simplify-button").on('click', () =>
    {
        console.log(getContent())
        $.ajax({
            type : 'POST',
            contentType: "application/json",
            url : 'http://127.0.0.1:5000/simplify',
            data : getContent(),
            success : (data)  => 
            {
                console.log(data)
            }
        });
    });
});