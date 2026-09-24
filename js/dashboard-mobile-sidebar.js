(function () {
  function isMobileView() {
    return window.matchMedia('(max-width: 640px)').matches;
  }

  function setSidebarState(isOpen) {
    const body = document.body;
    const sidebar = document.querySelector('.sidebar');
    const toggleButton = document.querySelector('.mobile-sidebar-toggle');

    if (!body || !sidebar || !toggleButton) return;

    body.classList.toggle('mobile-sidebar-open', isOpen);
    toggleButton.setAttribute('aria-expanded', String(isOpen));
    toggleButton.textContent = isOpen ? '✕' : '☰';
  }

  document.addEventListener('DOMContentLoaded', function () {
    const body = document.body;
    const sidebar = document.querySelector('.sidebar');
    const toggleButton = document.querySelector('.mobile-sidebar-toggle');

    if (!body || !sidebar || !toggleButton) return;

    toggleButton.addEventListener('click', function () {
      if (!isMobileView()) return;
      const isOpen = body.classList.contains('mobile-sidebar-open');
      setSidebarState(!isOpen);
    });

    sidebar.querySelectorAll('.nav-item').forEach(function (item) {
      item.addEventListener('click', function () {
        if (isMobileView()) {
          setSidebarState(false);
        }
      });
    });

    window.addEventListener('resize', function () {
      if (!isMobileView()) {
        setSidebarState(false);
      }
    });

    let scrollCloseTimer = null;
    window.addEventListener('scroll', function () {
      if (!isMobileView()) return;

      if (scrollCloseTimer) {
        clearTimeout(scrollCloseTimer);
      }

      scrollCloseTimer = setTimeout(function () {
        if (body.classList.contains('mobile-sidebar-open')) {
          setSidebarState(false);
        }
      }, 120);
    }, { passive: true });

    setSidebarState(false);
  });
}());
