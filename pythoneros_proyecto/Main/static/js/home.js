document.addEventListener("DOMContentLoaded", () => {
  const links = document.querySelectorAll('data-tema');
  const body = document.body;
  const temaGuardado = localStorage.getItem("tema");
  if (temaGuardado) {
    body.className = temaGuardado;
  } links.forEach(link => {
    link.addEventListener("click", e => {
      e.preventDefault();
      const tema = e.target.getAttribute("data-tema");
      body.className = tema;
      
      localStorage.setItem("tema", tema);
    });
  });
});