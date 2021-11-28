// URL root path of the current page
const page_url_root = window.location.protocol + '//' + window.location.host;

/*
    Triggered by the "Previous" and "Next" navigation buttons. Calls the naviation API
    to get the previous or next batch of tickets, and refresh the page upon success.
*/
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

/*
    Triggered by clicking on an <li> ticket listing. Calls the ticket details API,
    retrieves ticket details with associated HTML, and displays the rendered ticket
    details modal.
*/
async function ticketDetails(ticket_url) {
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
            ticketDetailsSection.innerHTML = body;
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

/*
    Triggered by the "X" (close) button in a ticket details modal. Closes the ticket
    details modal.
*/
function closeTicketDetails() {
    ticketDetailsSection = document.getElementById('ticketDetailsContainer');
    ticketDetailsSection.style.display = 'none';
}
