document.addEventListener("DOMContentLoaded", () => {
  const links = document.querySelectorAll(".dropdown-item[data-tema]");
  links.forEach(link => {
    link.addEventListener("click", e => {
      e.preventDefault();
      const tema = e.target.getAttribute("data-tema");
      document.body.className = tema; 
    });
  });
})