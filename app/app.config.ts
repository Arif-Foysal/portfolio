export default defineAppConfig({
  ui: {
    colors: {
      primary: 'cyan',
      secondary: 'green',
      neutral: 'slate'
    }
  },
  navigationMenu: {
      slots: {
        linkLabel: 'text-2xl font-bold',  // Change text size and weight
        link: 'px-4 py-2',                // Adjust padding
      },
      variants: {
        color: {
          primary: {
            link: 'text-red-600 hover:text-blue-800'
          }
        }
      },
      defaultVariants: {
        color: 'primary',
        variant: 'link'
      }
    }
})
