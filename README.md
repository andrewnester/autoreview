# Auto Code Review by ChatGPT

[![experimental](http://badges.github.io/stability-badges/dist/experimental.svg)](http://github.com/badges/stability-badges)

#### See how it looks like 👀

![](https://github.com/andrewnester/autoreview/assets/2969996/8201dbe9-b24b-493e-b575-e1d396f7b814)

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
