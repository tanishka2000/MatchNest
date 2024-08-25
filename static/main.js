document.addEventListener("DOMContentLoaded", function () {
    var body = document.querySelector("body");
    var modal = document.querySelector(".modal");
    var modalButton = document.querySelector(".modal-button");
    var closeButton = document.querySelector(".close-button");
    var scrollDown = document.querySelector(".scroll-down");
    var isOpened = false;

    var openModal = function () {
        if (modal) {
            modal.classList.add("is-open");
            if (body) {
                body.style.overflow = "hidden";
            }
        }
    };

    var closeModal = function () {
        if (modal) {
            modal.classList.remove("is-open");
            if (body) {
                body.style.overflow = "initial";
            }
        }
    };

    if (window) {
        window.addEventListener("scroll", function () {
            if (window.scrollY > window.innerHeight / 3 && !isOpened) {
                isOpened = true;
                if (scrollDown) {
                    scrollDown.style.display = "none";
                }
                openModal();
            }
        });
    }

    if (modalButton) {
        modalButton.addEventListener("click", openModal);
    }

    if (closeButton) {
        closeButton.addEventListener("click", closeModal);
    }

    document.onkeydown = function (evt) {
        evt = evt || window.event;
        if (evt.keyCode === 27) {
            closeModal();
        }
    };
});
