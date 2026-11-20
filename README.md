# LangChain 101: Learn Step by Step

Learn LangChain by running small Python examples, reading how they work, and changing them yourself. Start with a single model call and work toward an assistant that uses tools and remembers conversations after a restart.

The examples use Google Gemini through LangChain. The later lessons introduce LangGraph's checkpoint and store APIs for memory. Each file is a standalone lesson so you can explore one concept at a time.

## Before you start

You should be comfortable with Python functions, lists, dictionaries, imports, and running scripts in a terminal. No previous LangChain experience is needed.

You will need:

- Python 3.15, selected by `.python-version`. On Windows, install Microsoft C++ Build Tools with the **Desktop development with C++** workload and a Windows SDK so `uv` can build dependencies that lack Python 3.15 wheels.
- `uv` installed and available in your terminal.
- A Google Gemini API key and access to the model used by the examples.

The scripts currently configure `gemini-3.5-flash-lite` directly in each file. If your account cannot use that model, change the `model=` value in the lesson you are running to a model you can access.

## Set up your environment

### 1. Open the project folder

Open a terminal in the cloned repository:

```sh
cd langchain_101
```

Run every command in this tutorial from this folder.

### 2. Install the dependencies

```sh
uv sync --locked
```

This installs the dependencies from `uv.lock` into the project environment. Use `uv run` to run scripts without manually activating that environment.

### 3. Add your API key

Create a file named `.env` in the project root, or add this variable to your existing file:

```dotenv
GOOGLE_API_KEY=your_api_key_here
```

The model examples call `load_dotenv()` to load this variable. You can also set it in your shell. `.env` is already excluded from Git; keep your real key out of source files.

### 4. Make your first request

```sh
uv run python src/langchain_101/main.py
```

You should see a response type, generated text, and token usage metadata. The exact wording of model responses can vary throughout the tutorial.

## Your learning path

Follow these lessons in order. For each one, open the linked file, run it, trace the important lines, and try the exercise before moving on.

| Step | Lesson | What you will learn |
| --- | --- | --- |
| 1 | [Call a model](src/langchain_101/main.py) | Send a prompt and inspect the response. |
| 2 | [Work with messages](src/langchain_101/messages.py) | Use roles and pass conversation history. |
| 3 | [Build a basic chatbot](chatbot.py) | Keep a conversation going in a loop. |
| 4 | [Create prompt templates](src/langchain_101/prompt_template.py) | Reuse prompts with variables. |
| 5 | [Compose a chain](src/langchain_101/chain.py) | Connect a prompt, model, and parser. |
| 6 | [Get structured output](src/langchain_101/structured_output.py) | Return data described by a Pydantic schema. |
| 7 | [Call tools manually](src/langchain_101/tool_calling.py) | Execute a requested function and send its result back. |
| 8 | [Build an agent](src/langchain_101/agents.py) | Let an agent manage the model and tool loop. |
| 9 | [Add conversation memory](src/langchain_101/memory.py) | Save state and separate conversations by thread ID. |
| 10 | [Store user preferences](src/langchain_101/memory-store.py) | Save and retrieve data using namespaces and keys. |
| 11 | [Persist conversations with SQLite](src/langchain_101/memory-sqlite.py) | Resume a conversation after restarting the script. |

## Step 1: Call a model

Open [main.py](src/langchain_101/main.py) and run:

```sh
uv run python src/langchain_101/main.py
```

The script loads your environment variables, creates a `ChatGoogleGenerativeAI` model with `temperature=0`, and sends a string to `model.invoke(...)`.

The return value is a message object containing more than the answer text. Look at the three things the script prints:

- `type(response)`: the Python type returned by the model.
- `response.content[0]["text"]`: the text block accessed by this example.
- `response.usage_metadata`: token usage information for the request.

**Try it:** Replace the existing prompt with `Explain Python lists in two sentences.` Run the script again and compare the text and usage metadata.

**Checkpoint:** Can you explain the difference between the full response object and its text content?

## Step 2: Work with messages and roles

Open [messages.py](src/langchain_101/messages.py) and run:

```sh
uv run python src/langchain_101/messages.py
```

Instead of one string, this lesson sends a list of messages:

- `SystemMessage` sets instructions for the assistant's behavior.
- `HumanMessage` represents something the user says.
- The model returns an assistant message, which the script appends to the list.

The first user message includes a name. Before asking `What is my name?`, the script adds the first response and the follow-up question to the history, then sends the whole list again.

This is how the second request receives the context from the first. Your Python code is responsible for keeping and passing the history here.

**Try it:** Change the system message to make the assistant a patient Python teacher. Compare the follow-up answer with a separate call containing only `HumanMessage(content="What is my name?")`.

**Checkpoint:** Why does the second request need the earlier messages?

## Step 3: Turn the message list into a chatbot

Open [chatbot.py](chatbot.py) and run:

```sh
uv run python chatbot.py
```

The chatbot starts with a predefined `Hi`, prints Gemini's response, and waits at the `You:` prompt. Type `/end` to quit.

Trace one turn through the loop: send the message list to the model, append its response, read the next user input, and append that input. Each request includes the growing history.

**Try it:** Tell the chatbot your favorite programming language, then ask what language you mentioned. Restart the script and ask again without repeating the information.

**Checkpoint:** The list lives in the running Python process. Why does restarting the script lose the conversation?

## Step 4: Reuse prompts with templates

Open [prompt_template.py](src/langchain_101/prompt_template.py) and run:

```sh
uv run python src/langchain_101/prompt_template.py
```

Templates let you keep the instructions in one place and supply changing values separately. This file demonstrates two forms:

- `PromptTemplate` formats a string with variables such as `{topic}`, `{audience}`, and `{length}`. Its print and model-call lines are commented out in the example.
- `ChatPromptTemplate` builds messages with roles. The active example supplies `role`, `tone`, and `topic`, prints the resulting prompt value, and sends it to the model.

Invoking the chat prompt creates the model's input; the later `model.invoke(prompt_values)` makes the model request.

**Try it:** Change `tone` from `aggressive` to `friendly`, then change `topic` from `recursion` to `decorators`. Uncomment `print(formatted_prompt)` to inspect the plain string template too.

**Checkpoint:** Can you identify which values are reusable instructions and which are inputs that change on each run?

## Step 5: Connect the pieces into a chain

Open [chain.py](src/langchain_101/chain.py) and run:

```sh
uv run python src/langchain_101/chain.py
```

The central line is:

```python
chain = prompt | model | parser
```

The pipe operator composes the stages so each output becomes the next input:

```text
{"topic": "recursion"} -> prompt messages -> model response -> string
```

`ChatPromptTemplate` builds the messages, the model produces a response, and `StrOutputParser` turns that response into a string. The script prints both the result and its type so you can compare them with Step 1.

**Try it:** Change the topic in `chain.invoke(...)`. Then uncomment the `chain.batch(...)` example to run the chain for several input dictionaries.

**Checkpoint:** What job does the parser do, and what would the model return without it?

## Step 6: Ask for structured data

Open [structured_output.py](src/langchain_101/structured_output.py) and run:

```sh
uv run python src/langchain_101/structured_output.py
```

This lesson analyzes a customer review using the `ReviewAnalysis` Pydantic model. The schema describes four fields: `sentiment`, `rating`, `key_points`, and `summary`. The rating must be an integer from 1 to 5.

The script wraps the model with:

```python
structured_model = model.with_structured_output(ReviewAnalysis)
```

It then reads the returned object's attributes and exports the data with `model_dump()` and `model_dump_json(indent=2)`.

The current schema spells the positive sentiment label `"postive"`. That is the literal value accepted by this example; watch for it when inspecting the output.

**Try it:** Replace the review with a complaint about slow delivery and poor quality. Check whether the sentiment, rating, and key points reflect your new input.

**Checkpoint:** Why would a program processing reviews benefit from named fields rather than a free-form paragraph?

## Step 7: Let the model request a tool

Open [tool_calling.py](src/langchain_101/tool_calling.py) and run:

```sh
uv run python src/langchain_101/tool_calling.py
```

The `@tool` decorator exposes the `multiply` and `divide` functions as tools. The script makes them available to the model with `bind_tools(...)`.

Follow the complete round trip:

1. Send the arithmetic question to the model.
2. Inspect `response.tool_calls` for the requested tool name, arguments, and call ID.
3. Execute the matching Python tool with those arguments.
4. Create a `ToolMessage` containing the result and matching `tool_call_id`.
5. Append the model's tool request and the tool result to the history.
6. Invoke the model again to produce the final response.

For the existing `110 * 12` question, the multiplication result is `1320` when the model requests that tool. Binding the tools supplies their definitions; the Python code in this lesson performs the execution.

**Try it:** Change the question to `What is 144 divided by 12?` and trace which function runs. The division tool uses `//`, so it performs floor division.

**Checkpoint:** Can you point to the line that executes the tool and explain why the result includes the original call ID?

This small example handles only the first tool call and assumes one is present. If `response.tool_calls` is empty, indexing `[0]` fails; inspect the printed calls when experimenting with prompts.

## Step 8: Let an agent manage the tool loop

Open [agents.py](src/langchain_101/agents.py) and run:

```sh
uv run python src/langchain_101/agents.py
```

The previous lesson managed the tool round trip manually. Here, `create_agent(...)` combines the model, four arithmetic tools, and instructions to use those tools for calculations.

Inspect the printed message history to follow the agent's work: a user request, assistant tool calls, tool results, and a final assistant answer. A calculation can require several passes through that loop.

The final section uses `agent.stream(inputs, stream_mode="updates")` to print updates as the agent runs. This starts a second invocation of the same input, so running the whole file performs the task twice.

**Try it:** Replace the existing expression with `Add 25 and 15, subtract 10, then multiply the result by 2.` Trace the operations and check the final result against `60`.

**Checkpoint:** Which parts of Step 7 does the agent now handle for you?

## Step 9: Remember a conversation with checkpoints

Open [memory.py](src/langchain_101/memory.py) and run:

```sh
uv run python src/langchain_101/memory.py
```

This lesson gives an agent an `InMemorySaver` checkpointer. The configuration identifies the conversation:

```python
config = {"configurable": {"thread_id": "prtdv-session-1"}}
```

The script introduces a name, asks follow-up questions using the same thread, and then switches to a different thread ID. With the same checkpointer, calls on the original thread can use its saved state; the new thread has separate conversation state.

At the end, `agent.get_state(config)` retrieves a snapshot so you can inspect the saved messages. Unlike the manual list in Step 3, the checkpointer manages state between agent calls. This particular saver still keeps everything in RAM.

**Try it:** Change the introduced name, then compare the answers from the original thread and the new thread. Inspect the messages saved under the original configuration.

**Checkpoint:** What determines which conversation an invocation continues, and what happens when this Python process ends?

## Step 10: Store a user preference

Open [memory-store.py](src/langchain_101/memory-store.py) and run:

```sh
uv run python src/langchain_101/memory-store.py
```

This lesson does not call a model or require an API key. It creates an `InMemoryStore`, saves a preference, and retrieves it:

```python
namespace = ("user_123", "preferences")
store.put(namespace, "language", {"preferred_language": "Python"})
memory = store.get(namespace, "language")
print(memory.value)
```

Expected output:

```text
{'preferred_language': 'Python'}
```

The namespace groups data for a user and purpose; the key identifies an item within that group. A store can hold information you want to share across conversations. This example demonstrates the storage operations alone; it does not connect the preference to an agent.

**Try it:** Save a second preference under a `response_style` key, then retrieve both values. Use a second user's namespace to keep their preferences separate.

**Checkpoint:** How does storing a named preference differ from saving an entire conversation's state? Despite its use for information across conversations, this `InMemoryStore` loses data when the process ends.

## Step 11: Keep conversation memory after a restart

Open [memory-sqlite.py](src/langchain_101/memory-sqlite.py) and run:

```sh
uv run python src/langchain_101/memory-sqlite.py
```

This chatbot uses `SqliteSaver` to write checkpoints to `checkpoints.sqlite` in the current working directory. It uses the fixed thread ID `pratyush-session-001`.

Test persistence yourself:

1. Tell the assistant your name and something you are learning.
2. Type `/exit` to close the chatbot.
3. Run the same command again from the same folder.
4. Ask what your name is and what you are learning.

Keeping the same database and thread ID lets the agent continue the saved conversation. Change `thread_id` in the file to start a separate conversation in the same database.

**Try it:** Start a second thread, introduce different information, and then switch back to the original thread.

**Checkpoint:** Why are both the saved database and the thread ID needed to resume the right conversation?

## Compare the memory examples

| Example | What it keeps | How it is identified | Survives a process restart? |
| --- | --- | --- | --- |
| `chatbot.py` | A manually maintained message list | The list in the running process | No |
| `memory.py` | Agent conversation checkpoints in RAM | Thread ID | No |
| `memory-store.py` | Preference records in RAM | Namespace and key | No |
| `memory-sqlite.py` | Agent conversation checkpoints on disk | Database and thread ID | Yes |

## If you get stuck

| Problem | What to check |
| --- | --- |
| `uv` is not recognized | Install `uv` and make sure it is available on your terminal's `PATH`. |
| Python setup fails | Install Python 3.15, then run `uv sync --locked`. If a Windows dependency build reports a missing compiler, install the C++ Build Tools and Windows SDK described above. |
| Imports fail | Run `uv sync --locked`, then run the lesson with `uv run python ...` from the repository root. |
| Authentication or model request fails | Check `GOOGLE_API_KEY`, network access, API quota, and access to the `model=` value in that script. |
| A tool example fails at `tool_calls[0]` | Inspect `response.tool_calls`; the manual example assumes the model requests a tool. |
| The chatbot forgets after restarting | Only the SQLite example persists checkpoints to disk. Use the same working directory and thread ID when restarting it. |
| The `langchain-101` command fails | Use the file-based commands in this tutorial. The declared console entry point currently refers to a function the package does not define. |

Model requests require network access and may consume API quota. The SQLite database contains conversation history and is not currently excluded by `.gitignore`; review it before sharing or committing it.

## Put it together

After completing the lessons, try building a small study assistant using the pieces you have learned:

1. Use a prompt template to explain a topic at a chosen difficulty level.
2. Return a structured result containing a summary and practice questions.
3. Give an agent an arithmetic tool for calculation questions.
4. Add SQLite checkpoints so the conversation continues after a restart.

Use the lesson files as references, and explain what each component contributes as you add it. You have completed the learning path when you can trace an input through the prompt, model, tools, output, and saved conversation state.
