## To implement navigation:

1. Add navigation folder with python scripts inside your app
2. Add navigation folder with templates inside your `templates`-folder
3. Include the `content.html` and the `navigation.html` wherever you need
4. Create a navigation-blueprint and register it in your app
5. Create a tuple of your pages near the navigation-blueprint using `Page`-class and register them in the navigation-blueprint with `register_pages`-function

`content.html` - displays pages's content
`navigation.html` - displays navigation-menu

When you need to create a new page - declare it inside the `PAGES` tuple and provide data and template for it.
