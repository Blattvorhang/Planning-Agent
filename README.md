# Planning-Agent

## Environment Setup
To clone the entire repository, you will need to run the following command:
```bash
git clone https://github.com/Blattvorhang/Planning-Agent.git --recursive
```

If you forgot to add the parameter `--recursive`, you should run
```bash
git submodule update --init --recursive
```

Then install required packages:
```bash
pip install -r requirements.txt
uv pip install -e "./tools/arxiv-mcp-server/[test]"
```

Finally, you need to fill out your personal LLM API key in the `.env` file, as shown in [`.env.example`](./.env.example).
