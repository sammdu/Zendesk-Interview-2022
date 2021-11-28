async function gotoBatch(direction) {
    // construct the URL for asking the '/navigate' endpoint for the next/previous batch
    const hostname = window.location.protocol + '//' + window.location.host;

    try {
        // ask the server for the next/previous batch of tickets
        const response = await fetch(hostname + '/navigate?direction=' + direction);

        // if request was successful, refresh the page
        if (response.status == 200) {
            location.reload();
        }
        else {
            throw Exception(esponse.status);
        }
    }
    catch (e) {
        console.log(e);
    }
}
