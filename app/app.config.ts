export default defineAppConfig({
  ui: {
    colors: {
      primary: 'emerald',
      secondary: 'emerald',
      neutral: 'slate'
    },
    chatPrompt: {
      slots: {
        root: 'relative flex flex-col items-stretch gap-2 px-2.5 py-2 w-full rounded-lg backdrop-blur focus-within:ring-primary',
      },
      variants: {
        variant: {
          outline: {
            root: 'bg-default/75 ring ring-default focus-within:ring-primary'
          },
          soft: {
            root: 'bg-elevated/50 focus-within:ring-primary focus-within:ring-1'
          },
          subtle: {
            root: 'bg-elevated/50 ring ring-default focus-within:ring-primary'
          },
        }
      }
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
