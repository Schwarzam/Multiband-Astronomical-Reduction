const colors = require('tailwindcss/colors')

module.exports = {
  content: ["./src/**/*.{html,js}"],
  theme: {
    colors: {
      primary: '#1f2937',
      inactive: '#9ca3af',
      black: colors.black,
      white: colors.white,
      slate: colors.slate,
      gray: colors.gray,
      zinc: colors.zinc,
      neutral: colors.neutral,
      stone: colors.stone,
      red: colors.red,
      orange: colors.orange,
      amber: colors.amber,
      yellow: colors.yellow,
      lime: colors.lime,
      green: colors.green,
      emerald: colors.emerald,
      teal: colors.teal,
      cyan: colors.cyan,
      sky: colors.sky,
      blue: colors.blue,
      indigo: colors.indigo,
      violet: colors.violet,
      purple: colors.purple,
      fuchsia: colors.fuchsia,
      pink: colors.pink,
      rose: colors.rose,
    },
    extend: {
      fontFamily: {
        mono: "'DM Mono', monospace",
        logo: "'Josefin Sans', sans-serif",
        primary: "'Poppins', sans-serif",
      },
      height: {
        '9/10': '90%',
        '95/100': '95%'
      },
      gridTemplateColumns: {
        '1/5': '1fr 5fr'
      }

    },
  },
  plugins: [],
}
