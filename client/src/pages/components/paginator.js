
export function registerPaginatorKeybinds() {
    document.addEventListener('keydown', e => {
        switch (e.key) {
          case 'ArrowLeft': 
            document.querySelector('.paginator .prev')?.click();
            break;
          case 'ArrowRight':
            document.querySelector('.paginator .next')?.click();
            break;
        }
      });
}