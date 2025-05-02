# flightcrew
Autonomous agent swarm for finding flights to match user prompts. Right now this leverages

* a [CrewAI Hierarchical architecture](https://docs.crewai.com/how-to/hierarchical-process) for an agentic framework
* the [Amadeus API](https://developers.amadeus.com) for flight information 
* the [Groq API](https://console.groq.com/home) for inference.*

You will need to create an app (free) on amadeus as well as an account (free) on Groq in order to find the following information. Once you've gotten these, add a .env file with the following:

```shell
MODEL=groq/llama-3.3-70b-versatile
GROQ_API_KEY={{Groq API key}}
AMADEUS_BASE_DOMAIN=test.api.amadeus.com
AMADEUS_API_KEY={{Amadeus API key}}
AMADEUS_API_SECRET={{Amadeus API secret}}
```

The system will answer the question in `knowledge/inquiry` (to the extent it can do so). The response may be invoked with `crewai run` and will be found in a table in the file `report.md`.
