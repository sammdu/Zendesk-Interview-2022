// URL root path of the current page
const page_url_root = window.location.protocol + '//' + window.location.host;

async function gotoBatch(direction) {
    try {
        // ask the server for the next/previous batch of tickets
        const response = await fetch(page_url_root + '/navigate?direction=' + direction);

        // if request was successful, refresh the page
        if (response.status === 200) {
            location.reload();
        }
        else {
            throw Exception(response.status);
        }
    }
    catch (e) {
        console.log(e);
        // dislay a friendly error for the user
        const header_elem = document.querySelector("header");
        header_elem.innerHTML += '<p class="error">' +
            "Uh-oh! Failed to fetch the " + direction + " page. Please try again!" +
            '</p>';
    }
}

async function ticketDetails(ticket_url) {
    console.log("modal");
    try {
        // ask the server for the details of a ticket given its API URL
        const response = await fetch(
            page_url_root + '/ticket_details?ticket_url=' + ticket_url
        );

        // if request was successful, display the ticket
        if (response.status == 200) {
            // get the rendered ticket details HTML from the response body
            const body = await response.text();
            // inject the retrieved HTML into the ticket details container element
            ticketDetailsSection = document.getElementById('ticketDetailsContainer');
            ticketDetailsSection.innerHTML = body
            ticketDetailsSection.style.display = 'flex';
        }
        else {
            throw Exception(response.status);
        }
    }
    catch (e) {
        console.log(e);
    }
}

function closeTicketDetails() {
    ticketDetailsSection = document.getElementById('ticketDetailsContainer');
    ticketDetailsSection.style.display = 'none';
}
