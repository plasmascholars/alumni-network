# Alumni Network

Welcome to the Alumni Network for the Institute for Plasma Research (IPR) Gandhinagar. This platform is dedicated to connecting alumni, sharing resources, and fostering a supportive community for all members. Join us in celebrating our achievements and staying connected!

## Website

This repository publishes a website using MkDocs and GitHub Pages.

- Site content lives in [`docs/`](docs/).
- Alumni profile source files live in [`alumni-data/`](alumni-data/).
- Site configuration lives in [`mkdocs.yml`](mkdocs.yml).
- The GitHub Pages workflow lives in [`.github/workflows/deploy-pages.yml`](.github/workflows/deploy-pages.yml).

## How To Update Content

For normal website changes, you usually do not need to touch the CI workflow.

- Edit Markdown files in [`docs/`](docs/) to update pages such as the home page, events, news, and resources.
- Edit files in [`alumni-data/`](alumni-data/) to add or update alumni profiles.
- Edit [`mkdocs.yml`](mkdocs.yml) only when you want to change site navigation, metadata, or MkDocs behavior.

The files in [`docs/alumni/`](docs/alumni/) are generated automatically from `alumni-data/` during the MkDocs build. Do not maintain them by hand.

## Add A New Alumni Profile

These steps are for contributors who are new to Git and GitHub.

1. Clone the repository to your computer:

   ```bash
   git clone https://github.com/plasmascholars/alumni-network.git
   cd alumni-network
   ```

2. Create a new branch for your profile:

   ```bash
   git checkout -b add-your-name-profile
   ```

3. Copy the profile template and name the new file after yourself. Use hyphens instead of spaces in the file name:

   ```bash
   cp alumni-data/TEMPLATE.md alumni-data/Your-Name.md
   ```

4. Open `alumni-data/Your-Name.md` in a text editor and replace the template values with your details. Make sure the name field contains your full name:

   ```markdown
   - **Name**: Your Name
   ```

5. Check that Git sees the new file:

   ```bash
   git status
   ```

6. Stage and commit your new alumni profile:

   ```bash
   git add alumni-data/Your-Name.md
   git commit -m "Add alumni profile for Your Name"
   ```

7. Push your branch to GitHub:

   ```bash
   git push origin add-your-name-profile
   ```

8. Open a pull request on GitHub so the maintainers can review and merge your profile. After it is merged, the CI workflow will update the website automatically.

## Local Preview

To preview the website locally:

```bash
mkdocs serve
```

Then open `http://127.0.0.1:8000/`.

To do a strict build check locally:

```bash
mkdocs build --strict
```

## How The Build Works

- Every branch push and pull request runs an MkDocs build in GitHub Actions.
- Only pushes to `main` deploy the live site to GitHub Pages.
- During the build, [`scripts/generate_alumni_docs.py`](scripts/generate_alumni_docs.py) regenerates alumni pages from [`alumni-data/`](alumni-data/).

## Useful MkDocs References

- MkDocs Getting Started: https://www.mkdocs.org/getting-started/
- MkDocs Configuration: https://www.mkdocs.org/user-guide/configuration/
- MkDocs Writing Documentation: https://www.mkdocs.org/user-guide/writing-your-docs/
- GitHub Pages with custom workflows: https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages
