# Preface

Study how your basic model understands itself.
- Keeping the API structure of recursive realignment of the past Q&A cards of this conversation,
  make sure the "message", along with it's attribution into "role" and "content" tags identifying
  the same entity; make sure both your AI platform, such as Ollama or LiteLLM, and the model itself
  you have carefully chosen, mostly from Hugging Face: best platforms have their built-in ways to
  access Hugging Face models, or their own select few which are of fit architecture.
  - Keep the role-content structure if possible, or parse it to given format.
- For LitGPT, you need to implement message templates and follow it's internal format; it's meant
  for fine-tuning - sorrily you ain't the end user, you got the capability to directly access
  some form of basic tags, which should be standard interpretation, but not the only one:
  - You are meant to serve different formats of cards to access the realignment into it's training
    on "millions of examples with custom formats to distinct messages, system messages, special
    commands etc.
  - This is almost sure your litgpt model won't initially understand the basic syntax.

Things you need to add:
- They are basically configuration items to your access engines; you can switch between open source engines such as Jan, GPT4All and lmstudio.ai:
  - Jan is basically what we classically imagine as a "chattlebot": you choose small models, in current versions they have no library collection but hopefully
    it will be fast and lightweight; but it kind of supports session memory. Try to optimize it for speed: use small models, remove overhead, in future
    perhaps you don't need the document collection or you can utilize a small one to benefit from it's responsive display and optimization tags. Those are
    not so visible in exponential growth of memory and hardware use or large models, altough you can use one and try to optimize it for different goal.
  - GPT4All is able to serve one model, but I think you cannot locally use it then: I think it's basically not fine-tuned to be a server. It has document
    collections, but in current version the collections can become corrupt - you have to remove them manually and recreate.
  - Lm-studio, at first sight, is very similar chatting platform: looking closer, you can see it's optimized to provide you document embeddings, which act
    as document or document and content (pages are hashed or something like this) index; this needs some administrative abilities for configuration, or
    a hacker friend to set it up for you: perhaps a child of the neighbour. It needs a few configuration options, but might evolve into small logical puzzle
    to resolve with some study in, sometimes somewhat technical, documents. Basically you won't need much more than what you need to set up index on your
    filesystem - just turn it on -, or SQL table - also identify the type. This is the graphical interface also able to serve chat models, but command line
    tool Ollama might be better of it: it removes some graphical overhead and works hiddenly, so you won't notice how it works when you turn your computer
    on and off. It's registered as standard service: with LMStudio, it seems simpler that you turn on your graphical application, then it runs the installed
    servers and you can access them from other windows. It's ability to be invisible is not so sure and simple, as well as stability is often having causalities
    from graphical interfaces: still, it's the best you can get if you want an open source graphical user interface to extend the experience from Jan and GPT4All,
    linearly.

Each is more or less what the name says: LM Studio is rather an AI Studio; GPT4All makes GPT access for everybody; and Jan is, well, a common male name: if you want
to chat with a common, somewhat erudit man who gets stuck as there are more topics to resolve at the same time; this kind of bot appears to be a practical man,
who has studied a lots of dictionaries, but cannot much understand your personal matters above specific needs you can carefully state in a few sentences. But well,
start a new conversation and ask who was the first president of America: and hope it does not start to hallucinate if your matter is too decent.

# Three TODO: items

This is rather a textbook, and while I want to implement many things in code, it tends to leave you some homework: until *anybody* has solved this well enough, in small
piece of code to study the common things between us.

## First item

Register Q&A card tree as data structure, follow Pythonic understanding of it's semantics.

### Anytree connection

***Anytree*** is a small python library, which lets you:
- First and foremost: [Do this](https://anytree.readthedocs.io/en/latest/)
- Ability to create a tree structure from arbitrary Python objects using `Node` with the `Node("name", obj=instance)` pattern
- Support for assigning a single parent per node (`parent=...`) while allowing many siblings under the same parent
- Automatic maintenance of child lists when setting `parent`
- Access to structural relations: `.parent`, `.children`, `.siblings`, `.ancestors`, `.descendants`
- Tree traversal utilities: Pre-order, Post-order, Level-order, Zigzag, RenderTree
- Ability to store arbitrary attributes on nodes (e.g., linking your domain object via `obj=...`)
- Easy reconstruction of hierarchical paths using `.path` and `.ancestors`
- Filtering and searching nodes using `findall`, `find`, and custom predicates
- Exporting or visualizing the tree using `RenderTree`, `AsciiStyle`, `ContStyle`
- Ability to compute depth, height, and other structural metadata

Anytree is associating it's elements with this branching conversation, and creating a powerful database syntax based on this very same class,
it's inheritance and function: each time you create a member and associate it's parent, you create Anytree node, which associates with this instance
and also you make it know who is the Node of your parent, which is the creaded node's parent. Instantly, you have access to Anytree's powerful
branching, node structure with optimized query interface similar to XML search, yet simple. Just ask AI and don't read the funcing manual.

### MongoDB connection (optional)

***MongoDB*** is database, which gets heavily integrated into **Python** and *it's objects*.
- It supports **Pythonic** class structure, which gets associated with rows of class-like definitions rather in Python;
  - You can add random attributes, *randomly named new fields* inside every row, and to *keep some alignment into same class or header*,
    is completely at your own hands. Python class, unless it has it's own basic standard and you can do some for this,
    also just accepts any parameter name for any instance. So it's a pythonic database.
- It has real-time access, where the other process can follow when you add or remove members, change field names.
  - Through ***Flask***, you are perfectly capable to connect Backbone.js, it's collections and other relations already
    appearing in your *Javascript* and **HTML**, client side facility where you utilize our classic work for stylish outcome:
    *countless hours of human imagination empowered by an AI*. **MongoDB** has ***real-time interface*** to watch events, and
    *Flask is not very active itself*, it looks like a passive server: but it's ***fine enough to use Backbone's real-time
    abilities on client side***, and Python can freely organize it's threads and processes when it's using Flask. *It does
    not reinvent* that: Django can be very Pythonic, but it's also as hard to learn as React or Vue, and put you into
    a special database collection, where each of your objects must be carefully registered into grand library, ready
    ***for it's orchestration***. Does it feel like a dictatorship compared to lightweight library, which also capably connects
    each single variable into real-time connection: moreover, there was always the "***innerHTML***" **attribute** *in* ***HTML***, which
    allows *straight real-time control from **Javascript***, far from also registering the object in *grand enterprise*, an ordered library
    with strict definition of a "book". Are we AI programmers or graphical programmers: React and Vue programmer is particularly a specific
    Specialization, while Backbone.js gives you basic vocabulary to express your particular needs without raising a framework of definitions:
    so you can specialize yourself. Flask has removed even organized project structure entirely in later versions to avoid this "book-keeping"
    effort of central librarians and standardizers: we need a few interactive controls, and full framework is not worth it for single
    streaming of text; rather we can achieve *any single effect* separately, in minutes of AI.
    - Use your imagination: use the Force \[well, poor Star Wars parody\].
  - I am sure: AI is an end of content management: a boring system which uses *standard form* for text page.
    - Just take this time from this library:
      - Create a branched tree of query and reply.
      - Express each chapter idea into new node, while setting the summary and chapter collection as entry of main leaf, a kind of "you are"
        message like "you are the writer of this book, and you finish it in time".
        - Turn chapters and subchapters of last answer into new nodes: associate with summary of whole book, whole book past and forward,
          and contextual summary of this part; after this: the node contains title and content of this chapter, where it's noted where to
          add the text, and if there is page, titles or titles and 40-char summaries of each heading and it's content, for example.
        - This has ideally a tensor interface, easy to optimize: tension levels to make the summaries longer for each item. Logic language
          can be used to add tensors between nodes, and somehow request which nodes to add to context based on parallel logicalism, parallel
          of your text logic into a logical syllables: there is certain logic between the cards, but especially an optimization and performance
          effort rather than any hard calculation a normal person could not do. For example, it's certain "logic" that card is a "fix" for another
          card, or it "supports" it, moreover that it "needs to be considered in parallel". As much as those syllables and their results are
          using hardware, time and memory, as well as your reading and answering time for intelligent intuition of humans in your programs you
          need to achieve in this hardware use, which participiates in human programs and software programs and we interface this feature
          with override of "__call__" - in interesting syntax, you see a pair of bracets "()" appearing in end of sentence, becoming a "caller"
          for this AI class, where every generation of immutable new elements - once they are "closed" from AI work and register of local events,
          and inner tool use: they are immutable. Initially, they are lazy: you have to call this function once, wait until the response is over
          stream it until then, and after use the static answer in "answer" field and as a last message this class provides, or the last message
          before the in-frame modification of it's results. That this class is parent for the child executions of the AI, and it loses track
          more easily if the past is modified, you keep all the parent messages constant: once you update the parent, you add this update as a
          new branch from *it's **own** parent* and if you want to reinvent subbranches: either they are standard subqueries of this query, and
          you might want to inherit or reproduce them, but their content must be reanswered and they have new parents and positions; or you have
          the past questions as candidates, and you have to review each of how the situation has changes: worse, same, better; compared to their
          initial context, and how to rephrase or open new nodes as the wheel has been reinvented and the context is lost - there is another attribute
          or direction of intent, this is either a change of frame, or paradigmatic shift.
          - These tensors set up their intent of will to use these resources.
          - This intent meets outer qualification and is balanced with will of other tensors, it's a karmic effort between them and should be followed
            by karma, for the future and the past.
          - They also meet local and global memory constraints: they add to shared use of the same resource or initiation, if rebranching the parent
            can be done under the same identity, or they otherwise use the performance statistically, based on only their volability; they also
            use it locally: in each generation, they set up their local space capability based on various factors, for example how far in the past
            they are: conversation past has limits, for small model it has tight limits, and past messages, then the whole past back, must be
            summarized; this could be hidden subtask of your Q&A, or a separate task: for short summary, AI might be asked to do 7 of such tasks,
            if it meets the actual memory model: for example, in 1000 token window, you could do 10 100 token operations linearly if the small model
            is capable enough: it can do several different tasks.
          - Inertia: if same query is executed several times, allowing cold answers, it can keep the resources: for example, once two logically connected
            elements are analyzed together, summary of this connection is always the same until criterion updates.
          - Several items in the past, covered by rather list of Q&A than single card, and AIStreamer has object for each card, not question or answer alone -
            the latter has less standard form, where a Q&A creates very strong patterns in interfacing and fine-tuning a standard model, either language
            model or machine learning or image model: each time, you tend to have Q&A of some form based on NN-DL simplification, once mostly called
            (Digital) Neural Networks - mathematical simplification of equivalent human's and animal's \[theoretically yet similar\] neural networks.

