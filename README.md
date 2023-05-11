# Auto Code Review by ChatGPT

## Usage

### Example workflow

```yaml
name: Auto Review
on: pull_request
jobs:
  test:
    runs-on: ubuntu-latest
    permissions:
        pull-requests: write
    steps:    
      - uses: actions/checkout@master
      - uses: technote-space/get-diff-action@v6
        with:
          PATTERNS: |
            **/*.py
      - uses: andrewnester/autoreview@master
        with:
          apiKey: ${{ secrets.OpenAIKey }}
          files: env.GIT_DIFF
      - uses: mshick/add-pr-comment@v2
        with:
          message: ${{ steps.selftest.outputs.review_comment }}

```