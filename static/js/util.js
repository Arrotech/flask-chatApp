document.addEventListener('DOMContentLoaded', () => {
    let msg = document.querySelector('#message');
    msg.addEventListener('keyup', event => {
        event.preventDefault();
        if (event.keyCode === 13) {
            document.querySelector('#sendBtn').click();
        }
    })
})