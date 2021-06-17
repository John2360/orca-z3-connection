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
            url : 'http://blum.cs.haverford.edu:8080/checker',
            data : getContent(),
            success : (data)  => 
            {
                console.log(data)
            }
        });
    });
});