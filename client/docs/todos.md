# Issues

## Webpack
- SASS uses its own module name resolution mechanism which differs from the current webpack setup. Specifically `config.resolve.alias` rules will not apply to filenames in `@use "";` expression.
- Figure out how to set up source maps for production.
## HTML/Templates

### `user.html`
- AJAX search.

### `import` pages
- consolidate them into a single page, since most of them are jsut placeholder for AJAX scripts.

## CSS
- Inject env variables into the stylesheet.

## JS
