# Alpaca Integration Prototype — Project Showcase

A compact Python experiment for inspecting rule-based market indicators and broker-tool integration.

## What the source demonstrates

- SMA, RSI, and MACD rule calculations in [agent.py](./agent.py).
- Broker/account/history/order wrapper functions exposed through FastMCP in [mcp_server.py](./mcp_server.py).
- A paper-trading endpoint as the default. The endpoint can be changed through configuration, so this is not an enforced paper-only boundary.

The inspected agent calls Python wrapper functions directly. This showcase does not claim an LLM decision layer, proven end-to-end MCP transport, or a tested trading strategy. No trading account or order was contacted during the showcase review.

Runtime behavior and financial performance remain unverified. Treat this as source-code research and integration work.

## Project collection

- [Contact CSV cleanup and dashboard portfolio](https://practical-data-tools.pulsargeek.chatgpt.site): verified fictional examples, review queues, retained originals, and documented cleanup scope. **The portfolio is public and available to view.** The proposed $49 contact-cleanup service has no live checkout.
- [Market Research Dashboard / ForesightTape](https://github.com/adigp4-alt/drrrd): dashboard, forecast evaluation, and reporting source.
- [Alpaca integration prototype](https://github.com/adigp4-alt/alpaca-ai-agen): a compact rule-based Python/API experiment.
- [OpenClaw fork](https://github.com/adigp4-alt/openclaw): attributed fork of [openclaw/openclaw](https://github.com/openclaw/openclaw). Fork-specific adaptations and deployment are not established by this showcase.
- [Render MCP Server fork](https://github.com/adigp4-alt/render-mcp-server): attributed fork of [render-oss/render-mcp-server](https://github.com/render-oss/render-mcp-server). This account is not the official Render publisher.

The separately verified local project-tools workspace is distinct from the public OpenClaw fork. Capital Research Desk and Agent Observatory remain private. AXIOM Garage is an unpublished concept. Investing and Gambling are research project labels without a separately verified product offer.

## Explore or discuss the work

Inspect the linked source and documented project scope. For cleanup inquiries, describe the goal, approximate row count, headers, and deadline through the channel where this showcase was shared. Keep personal records out of public comments. Agree a private delivery channel before sharing a real file.

This is a software portfolio. It makes no claim of previous clients, earnings, investment returns, predictive accuracy, official upstream affiliation, or verified production deployment. Third-party projects retain their own attribution and licenses. Public visibility of a repository is not proof of an open-source license.

Prepared October 1, 2026 from current public source review.
