document.addEventListener('DOMContentLoaded', function () {
    const logo = document.getElementById('logo');
    if (logo) {
        logo.addEventListener('click', function () {
            const url = logo.getAttribute('data-url');
            window.location.href = url;
        });
    }
});
