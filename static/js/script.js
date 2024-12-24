document.addEventListener("DOMContentLoaded", function () {
    // Sidebar toggle functionality for smaller screens
    const sidebarToggle = document.querySelector(".navbar-toggler");
    const sidebarMenu = document.getElementById("sidebarMenu");

    if (sidebarToggle && sidebarMenu) {
        sidebarToggle.addEventListener("click", () => {
            sidebarMenu.classList.toggle("collapsed");
        });
    }

    // Dynamic content update with spinner
    const updateSection = () => {
        const mainContent = document.querySelector(".main-content");
        if (mainContent) {
            mainContent.innerHTML = "<div class='spinner-border text-primary' role='status'><span class='visually-hidden'>Loading...</span></div>";
            setTimeout(() => {
                mainContent.innerHTML = "<p>Dynamic content loaded!</p>";
            }, 1000);
        }
    };

    const updateButton = document.querySelector("#updateContentBtn");
    if (updateButton) {
        updateButton.addEventListener("click", updateSection);
    }

    // Active state toggling with delegation
    const sidebar = document.querySelector(".sidebar");
    if (sidebar) {
        sidebar.addEventListener("click", function (e) {
            if (e.target.classList.contains("nav-link")) {
                const sidebarLinks = sidebar.querySelectorAll(".nav-link");
                sidebarLinks.forEach(l => l.classList.remove("active"));
                e.target.classList.add("active");
            }
        });
    }

    // Placeholder functionality for charts
    const loadCharts = () => {
        console.log("Charts will load here if implemented.");
        // Example chart integration
    };
    loadCharts();
});
