let dryRun = (process.env.RELEASE_DRY_RUN || "false").toLowerCase() === "true";
let testPypi = (process.env.RELEASE_TEST_PYPI || "false").toLowerCase() === "true";
const pypiToken = process.env.PYPI_TOKEN;

let prepareCmd = "poetry version -- ${nextRelease.version}";
let publishCmd;

if (pypiToken) {
    prepareCmd += ` && poetry config pypi-token.pypi ${pypiToken}`;
    publishCmd = `poetry publish --build`;

    if (testPypi) {
        publishCmd += ` --repository testpypi`;
        prepareCmd = prepareCmd.replace("pypi-token.pypi", "pypi-token.testpypi");
    }

    if (dryRun) {
        publishCmd += " --dry-run";
    }
} else {
    // No PYPI_TOKEN secret configured: this is an academic project, not
    // published as a public PyPI package. Still build the package (so a
    // wheel/sdist is available to attach to the GitHub Release), but skip
    // the actual `poetry publish` step, which would otherwise fail.
    publishCmd = "poetry build";
}

import config from 'semantic-release-preconfigured-conventional-commits' with {type: 'json'};
config.tagFormat = "bridgeit-v${version}";


config.plugins.push(
    ["@semantic-release/exec", {
        "prepareCmd" : prepareCmd,
        "publishCmd": publishCmd,
    }]
)

if (!dryRun) {
    config.plugins.push(
        ["@semantic-release/github", {
            "assets": [
                { "path": "dist/*" },
            ]
        }],
        ["@semantic-release/git", {
            "assets": [
                "CHANGELOG.md",
                "pyproject.toml"
            ],
            "message": "chore(release): ${nextRelease.version} [skip ci]"
        }]
    );
}

export default config;