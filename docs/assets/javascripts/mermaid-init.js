(() => {
  const initialize = () => {
    if (!window.mermaid) return;
    const dark = document.body.getAttribute('data-md-color-scheme') === 'slate';
    window.mermaid.initialize({
      startOnLoad: false,
      securityLevel: 'strict',
      theme: dark ? 'dark' : 'default'
    });
    window.mermaid.run({ querySelector: '.mermaid' });
  };

  document.addEventListener('DOMContentLoaded', initialize);
  document.addEventListener('DOMContentSwitch', initialize);
})();
