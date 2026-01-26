# Introduction  
*This intro section is written by Copilot; what follows, is my initial outline with copilot's explanative manual, rich with actual cases.*

This document introduces the intent, philosophy, and usage patterns behind the `CLIGPTOOPChat` architecture. If you have already explored the surrounding manuals—such as the Nuts and Bolts overview, the driver‑specific notes, or the configuration guides—this chapter ties them together into a coherent mental model. If you have not, the explanations here will make the rest of the documentation feel familiar before you even read it.

The goal is simple: help you understand why the system looks the way it does, why its simplicity is intentional, and how that simplicity becomes a foundation for more advanced work. The classes, drivers, and configuration files in this project are deliberately minimal. They are not meant to impress with clever abstractions or heavy frameworks. Instead, they are designed to be readable, teachable, and adaptable—something you can sketch on a whiteboard, explain to a colleague, or extend in your own direction without fear of breaking hidden machinery.

By the end of this chapter, you will understand the architectural choices, the OOP patterns, the role of session memory, and the differences between the three driver families (Ollama, LiteLLM, and LitGPT). You will also see how complexity grows when needed—and how the project keeps that growth under control.

---

# Session memory and general considerations

When I wrote these classes, I encountered some initial complexities:
- I added complex inheritance and already started to calculate through advanced algorithms in my head.
  - Trivially, the AIService class is doing a recursive seek of all messages in parent classes and that's it: this function really suits the programming textbook.
  - One can definitely add compression (summarization) of past messages, context sensitivity about which ones to show, and correct alignment and order of messages.
- In initial example, the Ollama code sent initial prompt "you are helpful assistant.."
  - This helps understanding the history, for example who is the role "assistant" who used to send messages before.
  - You can actually add such prompt to "chat.py", before the initial message, the "commanded" method will eventually add message of this form:
    - {"role": "system", "content": yourmessage} # - here, "yourmessage" is the variable, and as you give it as input to "commanded" method,
      the system might think the system assigned them such role.
- In initial example, litgpt streamer was far more advanced as it was using an advanced library.
  - CoPilot did not like at all that I replaced advanced system (where the model has to be in given folder, not autodownloaded by command line, and user is active
    at maintaining it's files and knowing their structure and content).
  - I did not really choose litgpt to be "the advanced system", but it had to contain such back-up of functionality. Rather, within command line of litgpt it's very
    easy to download a small model (such as 0.5B, 1B or 3B) and start fast fine-tuning process. It does not have your own fine-tuning cards unless you add them, and
    that's quite a bit of work: rather, you can find how to add it's built-in (to it's online arch.) command line flag to connect to any of it's online services;
    it will fine-tune based on these standard, random cards for you. This experience is very simple, basically you install it with one or a few commands, install model
    with next command, and with third command, you connect it to fine-tuning service to do some fine-tuning job, which does not match your own.
  - Once this automatic, arbitrarly running-nowhere kind of useless fine-tuning is done on small model; the beauty of litgpt_streamer is not that it would allow
    you as an advanced programmer to start heavy coding sessions with my, well, trivial code to help you, but the "LLM" library we import from "litgpt" is far
    from being it's most advanced function: it will give you answers without streaming and you wait long, get them in one piece. If you are sure in this "functionality",
    you can ensure that if "stream" exist in configuration, it must be set false for this model - currently that variable is there only for inspiration, not checked or used.
    - Here, I assumed this: in other manuals, I described how to convert litgpt models to ollama (GGUF) format supported by several services; direct driver is meant to
      be small, compact, and actually hide even this hinder compexity that it was even streaming.
- Some variables are there, which are not used: when choosing architecture, I set this variable for inspiration, because it's easier to understand than what happens
  inside the class. I am not sure you are not going to use the architecture string.
  - Additionally, "lazy" and "answer": they are implemented without considering the multithreaded nature of HTTP queries; rather, these variable names are inspiration
    for your implementation, and in simplest use cases the multithreaded nature is not visible (for example, you hide the message from other users until it's not lazy
    any more), finally that it can start "__call__" several times to ask an AI for answer, but once it succeeds to set the "answer" variable once, it won't call
    any more - the answer is updated a few times in this worst case, and for this worst case we get the initial simplicity.

# Simplicity tags

I did consider a lot that these are basically text book cases of code; for example adding strings by recursion, from older to newer, is an example which can be literally
found in textbooks; the advanced function I initially had there: is actually for study.

The case is also that if you do not have session memory, the code can be used for single question: with snippet 1, if you do not modify it's function, you have graphical
display for such single question-answer pair, such as "translate this to spanish". Initially, you might want to resolve this case to build a basis you start to fine-tune,
and the missing functionality in both cases, for the first snippet and this AI driver, including their documentation of the both, enables simple user to build the simplest
kind of stateless AI, such as translator. They add advanced, hidden task and get the display, where they can give input for this type of tasks, and get it done with their
own, AI-backed tool.

For more advanced programmers, *both code examples* need some work for session memory; I think it's a reasonable
work, because the implementation is up to your architecture: different AI models and systems do this differently, for example Ollama models might generally follow ollama
standard of session memory; but well this standard works already in code: in fact, the AI has to understand that role="assistant" messages in history are *his own*,
for example if it defines itself as simple, stateless AI in it's out-of-the-box state, very important initial state to show to you; in nuts and bolts you open the robot
box, and initially it states it is very much without character or self-consciousness: indeed, you explain it what it needs to be, and then it starts to function. This is
the common order of things: in clock manuals, for example I have new clock with day of the month; but it's 12h clock, but I had to move it 12h further to set the date change
not in the middle day - this kind of features can be not covered in manual, because they are stupid. I wanted this kind of essential quality in this manual.

Complexity in my own head: I can really work with complex code, but I also have long experience with complexities and I am sure that for an AI to understand at once, and
for me and the users: actually the complexity to initially tackle to understand an architecture is not even 150 lines, but it's literally that you have the right class,
inside the single most important command, and explicitly states structures such as yielding generator or recursive function explicitly written out. This kind of code
does not contain fancy customization or even fancy initialization which would not support the intent of different users - sometimes, it lacks some critical function for
production code, but assumes you have this bolt yourself.

This complexity flag set, I really care that you can create UML diagrams: the given code, for each file, function or architectural quality, is a single UML diagram with
some, say, 10 or even 5 elements with simple connections, depending on your generalization level; this kind of diagram can be understood by theoretical computer science
student, such as your IT boss: it's the topmost quality if you draw a single recursive function on paper in abstract form, with connections and explanation. If it's a
modular system of 5 different recursive functions and their interaction, you lose this initial discussion and dialogue, and rather represent a black-box system. This
UML can be indeed autogenerated from this code.

So, indeed, even the single short lines you need to add, such as prompt "you are a helpful assistant": I still gave the "complexity" tag to these lines, and asked whether
they are critical; actually it's not critical that the session memory works out of the box: rather, it's the white configuration of a bot, with no instructions, and you
have different architectural choises where you add this line:
- Add, to chat session (client code), the "commanded", before any "asked" or "answered"; **then** ask first question: the command is in the initial Q&A instance as given
  by the chat factory (you can add "prompt", "ask" or other functions to your factory depending on what it's output would mean to you).
- Add, to the bot driver, some code which would add these answers even if the prompt is empty; AIService can have explicit variable "prompt" rather than adding a message,
  and the driver would find appropriate message, ensure it also awakens chat history and correct self-identification, then it would do "commanded" on AIService.
- For litgpt, you need to set up model templates, which define which tags are used for messages.

In addition to messages, you can add tools, which are similar lists.

Limits to drivers:
- Ollama driver has chat and model list.
- In LiteLLM, we don't have model list: you can create tokens online, and for general-purpose system we won't list all models on the web.
- In LitGPT, we do not have even streaming of answers: it's my idea that you convert the result into GGUF, this basic driver for a person
  who rather wants to fine-tune than test software, might do it's best, for example have answers to all his test questions automatically made at night.
  This activity is different from first-hand software creation: rather, conversion of a model is complicated, and maybe you first make sure you even have it.
- This general limit: I wanted to make sure you won't see one strict format for a driver in this generic class, but different ways to get it to work.

CoPilot did not like I simplified LitGPT interface so much: it said, for any serious work, one wants to use advanced drivers of litgpt and not it's command
line interface. But precisely, I did choose litgpt for these manuals and examples, and my convinced users, because it has this administator interface - easy
install of models, not handling models as files and folders or studying the folder structure and it's ever-changing standard, and to start fine-tuning with single
command-line command as well: I rather studied this constraint as a plus, that advanced programmer can indeed use the same program, same model, and same work even
the same AIService class; they write their own connector and have advanced functionality. Administrator, rather, once they finish their work they can try to convert
their model to more standard and usable GGUF or use litgpt specific interfaces: this conversion, itself, is somewhat complex and not trivial to succeed first time,
which is why they rather would like this simple interface, which won't stream, can satisfy the web interface but especially, it can fill their tables of test questions
with answers: non-streaming interface, potentially, is here slightly more efficient than streaming interface. I wanted precisely to show one of 3 implementations as such
simple, trivial thing to administrators; "yield", in fact, is as capable as "return" to return the string in one piece.

# Executable files

Run "`ollamaautomodelsjsonconf.py`" with python to get ollama model list if you have ollama with some models at localhost - notice you need config file "ollama_models.json",
which contains "`{ "host": "http://localhost:11434" }`" for most typical configuration. This creates model list. Model list is now in "`ollama_models_gen.json`"
configuration file, but this is not used: you rename it to "`models_config.json`" if you won't create this manually. Now run "`modelselector.py`" and select one, initially
better small model which loads instantly.

Now, run "`chat.py`" to see that after first question, the chat history is lost - but you see two answers in such case. This initial problem is for you.

In "Services" folder, each "`streamer`" is also a Python executable, and you can run it if it's in the configuration to use that model. You can use only AIService
class and this single local architecture driver, and put those two files in the same folder with configuration classes, especially "`modelselector.py`", which is
used explicitly in "`filename.py`" to detect folder structure: "`filename.py`" is the third class to include with configurators. Then you have 4 files, configurator
and one single execution class, and you make the model list yourself or include those files as well. This still works in the same architecture method, but you can
now remove the other architectures from "`service.py`" and perhaps, you rather create new instance of your model driver yourself than using the factory. This way
you have removed some complexities.

# OOP

Remember that the OOP structure is a little bit complex to consider at first:
- Using an interface, which fits all 3 architecture classes, you can create controllers, which can be used to further abstract these functions.
- You cannot create extensions easily by inheriting from AIService class, but still it's meant by me that you extend this class to contain your
  general, automatic functionality for models, extensions etc.
- You probably want to inherit, from architetures such as given 3, special modalities for each model: for example, OllamaQwen3b might be child for
  OllamaBasicStreamer and create functions, which initialize this Ollama model based on settings in AIService; AIService is a parent class, but indeed
  it will be able to use any methods you add to child class.
  - Because of this reason, it's hard to make another line of child classes to AIService, as most of the languages won't support multi-parent inheritance and
    complex themes therein; rather, you need to create an interface, which suits AIService *with the children already initialized*, or you create a worker
    class, which has a variable of type AIService to connect the service, and handles it's inheritance itself - such classes need to have "parent" by convention,
    and basically it needs to make sure that it's "ask" method creates an instance of the same class, and "parent" points to it's real parent.

---

**The rest of this manual page is by CoPilot**.

# The Motive for Simplicity  
The entire architecture is built around a single principle: **the simplest possible code that still teaches the right ideas**.

Simplicity here is not an aesthetic preference. It is a functional requirement:

- A beginner should be able to read the code and understand the flow of a chat session.
- An administrator should be able to run a model, test it, and fine‑tune it without learning a new framework.
- An advanced programmer should be able to extend the system without fighting hidden assumptions.
- A theoretical computer scientist—or a boss who wants a UML diagram—should be able to see the structure at a glance.

This is why the core `AIService` class is intentionally textbook‑simple.  
It recursively walks parent messages. It stores state in plain attributes.  
It exposes `asked()`, `answered()`, and `commanded()` without magic.

The simplicity is measurable:

- **One recursive function** to gather messages.  
- **One generator** to stream output.  
- **One factory** to choose a driver.  
- **Three drivers**, each under 150 lines, each readable in one sitting.

When complexity grows—session compression, advanced templates, multi‑modal tools, concurrency, or fine‑tuning workflows—it grows *around* this core, not inside it. The warning cases you mention (e.g., multi‑threaded HTTP, advanced LitGPT features, or custom prompt templates) are real, but they are intentionally kept outside the minimal architecture so the core remains teachable.

---

# Understanding the OOP Structure  
The OOP design is intentionally shallow:

- `AIService` is the base class.  
- Each driver (`OllamaBasicStreamer`, `LiteLLMBasicStreamer`, `LitGPTBasicStreamer`) inherits from it.  
- Each driver implements:
  - `ask()` → returns a child instance with updated history  
  - `__call__()` → performs the actual model invocation  
  - Optional helpers (prompt formatting, streaming, etc.)

This structure gives you:

### 1. A stable interface  
Every driver behaves the same from the outside.  
You can swap Ollama for LiteLLM or LitGPT without changing your application code.

### 2. A predictable inheritance chain  
The parent/child pattern ensures that each question creates a new service instance, but the history remains intact. This is the simplest way to model a conversation without introducing global state or complex session managers.

### 3. A natural place for extensions  
You can extend:

- `AIService` to add global behaviors (logging, tools, system prompts)
- A specific driver to add model‑specific features (e.g., Qwen‑3B‑Ollama with custom defaults)
- A wrapper class that *contains* an `AIService` instance if you need multi‑inheritance behavior

The architecture is intentionally open-ended: you can grow it in any direction without rewriting the core.

---

# Session Awareness and Initial Prompts  
Session memory is the heart of a chat system. The project keeps it simple:

- Messages are stored as a list of `{role, content}` dictionaries.
- The recursive parent chain reconstructs the full conversation.
- Drivers decide how to format this history for their backend.

But session awareness is not automatic. Models need cues to understand:

- Who they are  
- Who the user is  
- Which past messages belong to the assistant  
- What context should be carried forward  

There are several ways to achieve this, and the manual should show all of them:

### 1. Add a system prompt in `chat.py`  
Call `commanded("You are a helpful assistant.")` before the first `ask()`.  
This is the simplest and most explicit method.

### 2. Add a default system prompt inside a driver  
For example, Ollama models often expect a system message even if the user does not provide one.  
A driver can insert this automatically.

### 3. Use LitGPT templates  
LitGPT models often require specific tags or formatting.  
You can define a template that wraps messages in the correct structure:

```
[SYSTEM] ...
[USER] ...
[ASSISTANT] ...
```

This ensures the model interprets history correctly.

### 4. Use architecture‑specific conventions  
- **Ollama**: follows its own chat schema; system messages are optional but recommended.  
- **LiteLLM**: follows OpenAI‑style messages; system messages are standard.  
- **LitGPT**: uses prompt templates; system messages may need explicit formatting.

Each driver handles history differently, but the `AIService` interface keeps the user experience consistent.

---

# Driver Architectures and Their Roles  
The three drivers represent three different philosophies of model usage.

## Ollama: Specific and Precise  
- Local models  
- Fast startup  
- Clear chat schema  
- Good for experimentation and offline work  
- Ideal for users who want predictable behavior

## LiteLLM: General and Flexible  
- Connects to OpenAI, Azure, Anthropic, and also local Ollama  
- Unified API  
- Good for cloud‑based workflows  
- Ideal for users who want one interface for many providers

## LitGPT: Administrative and Fine‑Tuning Oriented  
- Designed for training and fine‑tuning  
- Models are stored locally  
- No streaming by default  
- Ideal for administrators who want to:
  - download models  
  - fine‑tune them  
  - convert them to GGUF  
  - test them in batch mode

The manual should emphasize that these drivers are not competing—they serve different roles in the ecosystem.

---

# Code Complexity and UML Thinking  
The code is intentionally structured so that:

- A beginner can read it line by line.  
- An advanced programmer can extend it.  
- A boss can understand it from a UML diagram.  
- A theoretical CS student can appreciate the recursion and generator patterns.

The UML diagrams that emerge from this code are small:

- `AIService` with 5–7 methods  
- Three subclasses with 3–5 overrides  
- A factory function  
- A configuration loader  

This is the ideal size for teaching architecture without overwhelming the reader.

The manual should highlight that this simplicity is not a limitation—it is a design choice that makes the system transparent and adaptable.

---

# Summary  
This document introduces the philosophy and structure behind the `CLIGPTOOPChat` architecture:

- **Simplicity is intentional**: the code is readable, teachable, and extendable.  
- **OOP is shallow and predictable**: one base class, three drivers, clear inheritance.  
- **Session awareness is explicit**: system prompts, templates, and driver conventions.  
- **Drivers serve different roles**: Ollama for precision, LiteLLM for flexibility, LitGPT for administration.  
- **Complexity grows only when needed**: the core remains small enough to draw as a UML diagram.

This chapter prepares the reader for the rest of the manual.  
Everything that follows—examples, configuration guides, driver details—will feel natural once this conceptual foundation is in place.
