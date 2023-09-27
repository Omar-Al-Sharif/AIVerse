module.exports = {
  root: true,
  env: { browser: true, es2020: true },
  extends: [
    "airbnb",
    'airbnb-typescript',
    "airbnb/hooks",
    'plugin:@typescript-eslint/recommended',
    'plugin:react-hooks/recommended',
    'plugin:prettier/recommended'
  ],
  ignorePatterns: ['dist', '.eslintrc.cjs'],
  parserOptions: {
    ecmaVersion: 'latest',
    sourceType: 'module',
    project: './front-end/tsconfig.json',
  },
  parser: '@typescript-eslint/parser',
  plugins: ['react-refresh', 'react', '@typescript-eslint', 'prettier',],
  rules: {
    'react-refresh/only-export-components': [
      'warn',
      { allowConstantExport: true },
    ],
    'react/react-in-jsx-scope': 0,
  },
}
