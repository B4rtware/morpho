Create a new release
====================

1. Run the following command `poetry bump <version>`
<br>*Morpho* uses the following schema: `^\d+\.\d+\.\d+(-(b|a)\.\d+)?$`

2. Bump the version within the file: `morpho/__version__.py`
<br>Make sure its the same which was used bumping with poetry

3. Open `Changelog.md` and write the new changelog:
    - Use the following `#` header: `v<version> - (dd.mm.yyyy)`
    <br>Used `##` headers:
    - 💌 Added
    - 🔨 Fixed
    - ♻️ Changed

4. Stage the modified files and push them with the following commit message:
    > chore: bump to version `<version>`

5. Run the following command `poetry build` to create a tarball and a wheel based on the new version

6. Create a new github release and:
    1. Copy and paste the changelog content **without** the `#` header into the *description of the release* textbox
    2. Use the `#` header style to fill in the *Release title* (copy it from the `Changelog.md`)
    3. Copy the version with the `v`-prefix into the *Tag version*

7. Attach the produced tarball and wheel (`dist/`) to the release

8. Check *This is a pre-release* if its either an alpha or beta release *(a|b)* - ***optional*** 

9. **Publish release**