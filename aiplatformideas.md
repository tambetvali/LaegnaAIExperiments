I do not want to set any standard, but let's discuss some ideas and implications of an AI-collaborative platform.

# File Format

Task to CoPilot:

```
Let's try to learn from Obsidian, Notion.so, LogSeq and mere file tree in VSCode with folders and md files.

Let's set this filetree standard:
- Folder names might have extensions.
- If md or other file is same-named with a folder, it becomes it's root document.
- If folder contains init.md, it's the root document equivalent for .md folders and folders without extensions. Related to init.md inside a folder, the equivalent root document is outside.
- Inside folder, having same-level title line right before same-level title line with only one line feed between, it becomes database identifier: it refers to a file or folder in link-relational position, including ; and : syntax.
  - Database folders or files are included to end of chapter, either collapsed, open, or level-in link projecting foldername to link parts in easiest way.
- Equivalent documents are mixed, and same-database-itemmed or same-named titles are ordered in aligned way.
- If folder is cat.png and file inside is init.png, init file - index or README equivalent -, contains a cat.
- In foldernamed file in parent directory needs to be linked in both equivalent files, ":" is used before link, and if init.ext needs to be linked, ";" is used. Otherwise, ../ is used for child-to-parent, and ./ is shortcut to link from parent main file to child file.

# Folder.png/
# Folder Title

This two-lined intro associates given folder, and without /, a file
- It's content is pasted to this part as subblock or "Dig into ->" button in end of that chapter.

#

Empty same-level chapter tag is used to close the chapter.
```

CoPilot answered:

## Unified File‑Tree Knowledge Standard (Draft Specification)

This chapter restates the full article in your requested structural format, preserving meaning while fitting your folder‑chapter conventions.

### Folder Names May Have Extensions

Folders may include extensions such as `.md`, `.png`, `.todo`, etc.  
This allows folders to behave like typed objects, similar to Notion databases or Obsidian type‑folders.

```
Examples:
Project.md/
cat.png/
Research.todo/
```

### Root Document Resolution

A folder’s root document is determined by the following hierarchy:

1. **Same‑named file exists** → that file is the root.  
2. **If absent, but init.md exists** → init.md is the root.  
3. **If folder has an extension** → init.ext inside represents the file‑equivalent content.

```
Example:
cat.png/
  init.png
→ init.png is the root document for cat.png/
```

### Title‑Based Database Identifiers

Inside a root document, **two same‑level headings separated by exactly one blank line** define database items.  
These items correspond to files or folders with matching names.

```
## Task A

## Task B
→ Task A and Task B are database entries.
```

Link syntax:

- `:filename` → link to folder‑named file  
- `;init.ext` → link specifically to init file  
- `../` → child → parent  
- `./` → parent → child  

### Equivalent Document Merging

Documents representing the same conceptual object (same name, same database identifier, same folder/file pairing) are treated as **one merged view**.

This mirrors LogSeq’s “page = file = block” model while retaining Obsidian’s folder structure.

### Folder‑Named File Linking Rules

If a folder is named like a file:

```
cat.png/
  init.png
```

Then:

- `cat.png` (outside) and `init.png` (inside) are equivalent  
- Both must link to each other  
- `:` links to the folder‑named file  
- `;` links to the init file  

### Two‑Line Intro Block

A folder or file is introduced by:

```
# Folder.png/
# Folder Title
```

or for files:

```
# File.png
# File Title
```

This associates the folder/file with a human‑readable title and defines the chapter boundary.

### Closing a Chapter

A single same‑level heading with no title:

```
#
```

…closes the chapter.

### Summary

This system blends:

- Obsidian’s folder‑based thinking  
- Notion’s database‑row model  
- LogSeq’s block identity  
- VSCode’s raw transparency  

It forms a filesystem‑native, markdown‑first, database‑capable knowledge graph format.

# Tags inside

```
%# precedes parameter, which contains tags, %#...#% has them inline (encapsulated / mechanistic commands).
%$ precedes AI or spacy commands, %#...#% has them inline. Commands are converted to some markup by an AI (creative / dollar commands).
%$$ Precedes a human task: find a replacement to this

SpaCy could be used for example as fast, context-independent dictionary model. In each case, the format is such:

%$ ChatBot: message

%$ Myname, ChatBot: message

%$ Myname, : message

[/Tag] - opens a tag
[Tag/] - closes a tag
[Tag//] - break between two parts or metaphoric "paragraphs" in a tag
[/Tag/] - tag input placeholder, which displays the value assigned to Tag, or it's output as well, as two senders. Content must be added to the Tag.

(/Attr) - opens an attribute
(Attr/) - closes an attribute
(Attr//) - break between two parts or metaphoric "paragraphs" in an attribute
(/Attr/) - attribute input placeholder, which displays the value assigned to Attr, or it's output as well, as two senders.

(/Attr) - starts a marker
(Attr/) - closes a marker
(Attr//) - break between two parts or metaphoric "paragraphs" in a marker
(/Attr/) - creates new instance for the marker in a list.

Tags and markers have attributes inside:
[/Tag]
  (/Attr)Attribute value(Attr/)
[Tag/]

This is referred to as Tag.Attr.

If whole chapter has only one Tag inside, especially if it's not with inline start and end, it has the chapter title and database item contained in it's header fields, and whole content matched.

Markers mark pieces of the document, which can be structured by reference markdown document into marker collection in free md format, which might for example include all pieces and provide commands to read and forget surrounding content to a GPT model

Tag, attribute and marker startings and endings are not necessarily hierarchical, but free-form chaotic like early html. Node reader might give multiple paths how they are contained, based on constraints such as node.[begin]subnode for this kind of structure, matching beginnings:

%# [/node]
%# [subnode/]
%# [/node]
%# [subnode/]

Because it's not strict match of containment of child in parent node.

Names, hashes and threads come after space, or if space is the first letter:

%# [/node name#class.thread]

This node exists only within list of threads, or class of threads, and it's name identifies it's variable name in parent element.

If, while, ext. tags are used inside blocks, for example if block contains "if" tag, it's only executed if it's inner command and attributes are met.

If attribute has the content on same line, it's hidden from final markdown.

Each tag or other element can join parents if tag has \\parentname\\it'sparentname list attached, in which case it appears as direct child of this parent; this might be set to happen leaving one processing phase in between, in list of conversions. \\/folder might link to parent folder, database identifiers might be extended to link external documents.

The whole idea: AI will convert AI commands to normal tags, attributes and markers, and then it will be processed by automata, AI, mixture, and user.

What is created: subthreads with AI training cards.
```

## Command‑Tag‑Marker Syntax for AI‑Structured Documents

This chapter describes the full command, tag, attribute, and marker system you outlined, expressed in the same structural format as the previous article. All sub‑blocks are escaped so they appear literally.

### Parameter Commands: %# … and Inline %#…#%

`%#` introduces a **mechanistic parameter command**, typically used for structural metadata, tags, or strict machine‑interpreted instructions.

Inline form `%# ... #%` encapsulates the parameter inside the text flow.

```
%# parameter
%#tag=value#
```

These commands behave like rigid, deterministic operators—useful for structural parsing.

### AI / SpaCy Commands: %$ … and Inline %$…#%

`%$` introduces **AI‑interpreted commands**, including SpaCy lookups, dictionary expansions, or creative transformations.

Inline form `%$ ... #%` embeds the command inside a sentence.

```
%$ ChatBot: message
%$ Myname, ChatBot: message
%$ Myname, : message
```

AI converts these commands into markup, tags, or attributes depending on context.

### Human Tasks: %$$

`%$$` marks a **human‑required action**, such as filling in missing content or choosing a replacement.

```
%$$ Find a replacement for this phrase
```

These tasks remain unresolved until a human completes them.

### Tag Syntax

Tags define structural blocks. They resemble early HTML—free‑form, non‑hierarchical, and tolerant of chaotic nesting.

- `[/Tag]` opens a tag  
- `[Tag/]` closes a tag  
- `[Tag//]` inserts a break inside a tag  
- `[/Tag/]` is a placeholder that displays the tag’s assigned value or output  

```
[/Note]
  This is a note.
[Note/]
```

### Attribute Syntax

Attributes behave like sub‑fields inside tags.

- `(/Attr)` opens an attribute  
- `(Attr/)` closes it  
- `(Attr//)` inserts a break  
- `(/Attr/)` is an attribute placeholder  

```
[/Person]
  (/Name)Alice(Name/)
  (/Role)Researcher(Role/)
[Person/]
```

This is referenced as **Person.Name** or **Person.Role**.

### Marker Syntax

Markers identify document fragments for later extraction, training, or recombination.

- `(/Mark)` opens a marker  
- `(Mark/)` closes it  
- `(Mark//)` breaks it  
- `(/Mark/)` creates a new instance in a list  

```
(/Example)
  This is a marked piece of text.
(Example/)
```

Markers can be collected into external documents for AI training workflows.

### Tags and Markers with Attributes

Tags and markers may contain attributes inside them, forming a flexible metadata structure.

```
[/Block]
  (/Type)Definition(Type/)
  (/Importance)High(Importance/)
[Block/]
```

This yields:

- Block.Type  
- Block.Importance  

### Single‑Tag Chapters

If a chapter contains only one tag (not inline), the chapter title and database item are derived from that tag’s header fields. The entire chapter content is matched to that tag.

This allows a chapter to behave like a database row.

### Marker Collections and GPT Interaction

Markers can be extracted into a separate Markdown file that acts as a **marker collection**.  
This collection may include:

- all marked pieces  
- commands to read or forget surrounding context  
- instructions for GPT models  

This enables training‑card‑like subthreads.

### Non‑Hierarchical Tag Structure

Tags do **not** require strict parent‑child containment.  
Like early HTML, they may overlap or interleave.

A node reader may infer multiple containment paths based on constraints such as:

```
%# [/node]
%# [subnode/]
%# [/node]
%# [subnode/]
```

This allows flexible graph‑like interpretation rather than strict tree parsing.

### Names, Hashes, and Threads

Names, classes, and threads follow a space after the tag:

```
%# [/node name#class.thread]
```

- `name` identifies the variable name  
- `class` groups nodes  
- `thread` places the node inside a thread list  

These nodes exist only within their thread or class context.

### Conditional Tags (if, while, etc.)

If a block contains an `if` tag, it is executed only if its inner commands and attributes satisfy the condition.

This allows logic‑driven document generation.

### Hidden Attributes

If an attribute’s content appears on the same line as its opening tag, it is hidden from final Markdown output.

```
(/Secret)hidden value(Secret/)
```

Useful for metadata that should not appear in rendered documents.

### Parent Joining via \\parentname\\ Syntax

Any tag or element may join additional parents using:

```
\\parentA\\parentB
```

This makes the element appear as a direct child of those parents in a later processing phase.

This supports:

- cross‑folder linking  
- external document references  
- database identifier expansion  

### Overall Workflow

1. **AI commands** (`%$`) are converted into tags, attributes, and markers.  
2. **Automata and AI** process the resulting structure.  
3. **Users** refine, correct, or extend the document.  
4. **Markers** become training cards or subthreads.  

### Result: AI Training Subthreads

The final output is a set of **subthreads**, each containing:

- structured markers  
- extracted content  
- metadata  
- commands for reading or forgetting context  

These subthreads can be used for:

- AI training  
- memory systems  
- document transformation  
- knowledge graph construction  

# Marker processing versioned editor

```
Version control system updates file versions based on time-defined or period-defined (if time is not always available), timespan-compatibly but equally numbered parts; it's made of letters and numbers, which can be prefixed with half-overlapping distinction of larger, further time periods, and distinction into smaller time elements and identifiers with normalized linearity inside time unit, which are all encoded into one: preferrably a two-letter piece inside current time period, for infrequent commits.

Versions for the whole or each file can be dot-separated into parts, which each have the same property of time.

Current timestamp might refer to last version, if used without specification, and old document have digits added before, while commenting often adds some after each part. Latest document, and latest version of each version-branched line, has it's latest timestamp used each time.

Unused parts of version refer to the last version, so the version nor branch might not be contained in link.

Different users can host branches on different hosts:
- Those are added as replies
- Parent nodes in other branches might be set
- Intermediate server or user provides authorization cards

Free distribution:
- Each server is open source and provides whole source code to be fully executed in clients.
- Many servers can register clients to different servers, other services might notice the servers if their registered clients appear; the server has a list of standard contributors they support, which might be their own.
- Server-side generation with low-level tool is still allowed for pages

Locally used pages can reflect the open source resources and create local clones of folders and repositories.
```

## Time‑Encoded Version Control System

This chapter describes a versioning model where timestamps, time‑period identifiers, and linearized sub‑units are encoded into compact version strings. The structure mirrors the same chapter format as earlier documents, with escaped sub‑blocks preserved.

### Time‑Defined and Period‑Defined Versioning

The system updates file versions using **time‑defined** or **period‑defined** increments.  
When exact timestamps are unavailable, a compatible period marker is used instead.

Versions consist of:

- letters and numbers  
- optional prefixes representing larger time periods  
- optional suffixes representing smaller time elements  
- normalized linear identifiers inside each time unit  

For infrequent commits, the preferred encoding is a **two‑letter piece** representing the current time period.

```
Example:
A3 → period A, third unit  
QF → quarter F  
TZ → time‑zone‑aligned period marker
```

### Dot‑Separated Version Parts

A version string may contain multiple dot‑separated parts:

```
A3.02.CF
```

Each part:

- corresponds to a time‑based unit  
- follows the same encoding rules  
- can represent the whole document or a specific file  

This allows hierarchical time‑based versioning.

### Timestamp Defaults and Version Inference

If a version is referenced without specification, the **current timestamp** refers to the **latest version**.

Older documents:

- may have digits added *before* each part  
- comments may add digits *after* each part  

The latest document in any branch always uses the **latest timestamp** for that branch.

Unused version parts implicitly refer to the last known version, so:

- a link may omit version  
- a branch may be omitted  
- the system resolves the missing parts automatically  

### Distributed Branch Hosting

Different users may host branches on different servers or nodes.

Branch‑related rules:

- Branches hosted by others are added as **replies**  
- Parent nodes in other branches may be explicitly set  
- Intermediate servers or users may issue **authorization cards** to validate branch lineage  

This creates a federated, multi‑host version graph.

### Free Distribution and Open Source Servers

Servers follow an open distribution model:

- Every server is open source  
- Full source code is available for execution on clients  
- Servers may register clients to multiple servers  
- External services may detect servers when registered clients appear  
- Each server maintains a list of **supported contributors**, often including itself  
- Server‑side generation using low‑level tools is still allowed for pages  

This encourages interoperability and redundancy.

### Local Clones and Resource Reflection

Local pages can:

- reflect open‑source resources  
- clone folders and repositories  
- maintain local mirrors of remote structures  

This supports offline work and decentralized collaboration.

# Editor

```
Editor looks like Zeal: local open document shapter tree in left-lower panel, whole chapter tree with filesystem levels in main chapter tree, where 6 levels of titles are repeated for each level, with their containment policy with database IDs.

On right side, the capters are given; or chapters above, marker list to see highlighted documents - below.

There are Code (mdc) view for everything, MD (md) view for default generasted document, and Rendered view for rendered conversion to HTML pr rendered markdown.

Under each such content, there is an instruction forum, where instruction can be given: either tasks to AI, or personally fulfilled (such as "A new comment", with content as answer).

This supports labelling, especially:
- For dumb autogenerated content, "Q&A are limited to language of this SpaCy agent", or "Only this math theory of possibilities are covered", or "Language is restricted to this subset of english, which is known to this agent".
- For intelligent autogenerated content, an AI can create cards and be aware in it's own score of labels - how good quality it can bring, how deep is the current contemplation on topic.

Other providers can use root node system to assign new solutions, and one solution can be chosen by provider - not necessarily his own, local one. He might use services where clients need to register and earn reputation, or which might even be able to check back for suggested positions of each nodes for AI firewalling from trolls and spam providers.

Markers, marker beginnings, ends and card template structures might be applied in editor: it keeps track of changes, which are also noted by compare and commit logs if not supported; supported editor allows to copy and paste markers, creating numbered instances or number for nameless entities. Markers are stored in separate file. where each point marker can have content, be part of collections, which are used to highlight documents and provide AI contexts.

Simple implementations would not rematch markers, but marker header might suggest beginning and starting point, containing context text and pointers coordinates there as well, and meaningful hints such as function name which is fully and only covered: this kind of functions and AI support might update markers, leave tasks, or remove suspicious entities based on their free will. User habits and fixes might be learnt.

AI system can form subthreads, which come by assumption:
- Initial MD file, folder or other type of file is perceived as context.
- It forms session, which is continued: linearly or hierarchically, where hierarchy-next element perceives previous, upper-level conversation and all it's tool use and calculations as his, and linear element uses the element before as pastnext message.
- Each added thread can be continued linearly, under same name, or broken into branches - replies to local message.

Helper tools and tags, as well as fine-tuning, might be incorporated to extract filefolder structures, local apis and attributes, and get them context-connected.

If left such tasks, not only the local AI answers each request point, but at each point where request is made, a set of AI providers and other tools might be mutually connected to get answers in their clients. Client, actually, can connect to server-side providers, and register it's users and instances in servers, which might also mirror the content while offline. Still, the thing is ran at client side, where server can contain it's main Robot client which has administrator rights
```

## Editor Architecture and Interaction Model

This chapter describes the structure, behavior, and workflow of the editor environment, following the same format and style as previous chapters. All sub‑blocks are escaped to preserve literal meaning.

### Zeal‑Style Multi‑Panel Layout

The editor resembles **Zeal**, with a multi‑panel interface designed for navigating complex document trees and AI‑assisted structures.

Left‑lower panel:
- Displays the **local open document chapter tree**
- Shows only the currently opened file’s internal structure

Main left panel:
- Displays the **full chapter tree**, mirroring filesystem hierarchy
- All **six levels of Markdown titles** are repeated for each filesystem level
- Containment rules follow database‑ID logic

```
Example:
# Level 1 (folder)
## Level 2 (subfolder)
### Level 3 (file)
...
```

Right panel:
- Shows the **current chapter content**
- Above: chapter text
- Below: **marker list**, highlighting referenced or extracted document pieces

### Multi‑View Document Modes

Each document can be viewed in three synchronized modes:

- **Code view (mdc)** — raw source with tags, markers, attributes  
- **Markdown view (md)** — normalized, generated Markdown  
- **Rendered view** — HTML or rendered Markdown output  

These views allow precise editing, structural debugging, and final presentation.

### Instruction Forum Under Each Content Block

Beneath each view, an **instruction forum** appears.

It accepts:
- **AI tasks** (commands, transformations, queries)
- **Human tasks** (e.g., “A new comment”, with user‑written content)

This forum supports:
- collaborative editing  
- annotation  
- incremental refinement  
- AI‑assisted restructuring  

### Labelling and Content Quality Metadata

Labels can be attached to content, especially autogenerated material.

For **simple or constrained AI agents**, labels may include:

- “Q&A limited to language of this SpaCy agent”
- “Only this mathematical theory of possibilities is covered”
- “Language restricted to this English subset known to this agent”

For **more capable AI**, labels help the system track:

- quality of generated content  
- depth of reasoning  
- confidence or awareness of limitations  

These labels influence how the AI creates cards, summaries, or training subthreads.

### Provider‑Based Solution Assignment

External providers can use the **root node system** to propose solutions.

- Multiple solutions may exist for a node  
- A provider may choose **any** solution, not necessarily their own  
- Providers may require client registration and reputation  
- Some systems may verify node positions to prevent spam or trolling  

This creates a federated, reputation‑aware ecosystem.

### Marker System and Marker File

Markers are fully integrated into the editor.

They support:
- marker beginnings and endings  
- card templates  
- change tracking  
- compare and commit logs  

Supported editors allow:
- copying and pasting markers  
- automatic numbering  
- creation of nameless marker instances  

Markers are stored in a **separate file**, where each marker:

- may contain content  
- may belong to collections  
- may highlight documents  
- may provide AI context  

### Marker Matching and Simple Implementations

Simple implementations do not rematch markers.  
Instead, marker headers may include:

- beginning and ending hints  
- context text  
- pointer coordinates  
- function names or semantic hints  

AI support may:
- update markers  
- leave tasks  
- remove suspicious entities  
- learn user habits and correction patterns  

### AI Subthread Formation

The AI system forms **subthreads** based on assumptions:

1. The initial MD file, folder, or other file type is the **context**.  
2. A **session** is formed, which continues:
   - **linearly** (each message follows the previous)
   - **hierarchically** (child thread inherits parent context, tools, and calculations)

3. Each thread may:
   - continue linearly under the same name  
   - branch into replies  
   - form parallel explorations  

This mirrors conversational trees and versioned reasoning paths.

### Helper Tools, Tags, and Fine‑Tuning

Helper systems may extract:

- file/folder structures  
- local APIs  
- attributes  
- contextual metadata  

These are used to connect content, automate linking, and enhance AI understanding.

### Distributed AI Providers and Client‑Server Interaction

If tasks are left unresolved:

- Local AI answers each request  
- Additional AI providers may be invoked  
- Tools may collaborate to produce answers  

Clients can:
- connect to server‑side providers  
- register users and instances  
- mirror content offline  

Servers may host a **main Robot client** with administrative rights, while computation still runs primarily on the client side.
```

# Your own creative format

```
Now your own creative format.

Describe, how hashed or classed tags can form virtual tables for processing by their class, which can be even accessed in sql-like structured manner, and is not necessarily protected for open source version: we do not provide server-side scripting or accessibility rights here, but client cannot easily mess with open-source server, which is connectible database to much more powerful AI processors, who make metadeductions.

Describe and give examples, how tags are used to have, for the same chapter: the answer, the instruction, the question (in different chances, either instruction or question is properly given, but the same answer is used), and superchapter is tagged to give one-line prefix or summary of list, for each encorporated title: another triggered extension adds this before each question in the list, with two line feeds after or two spaces after a line.

Two formats by it's database item's classes of chapter, which connect it to two providers similarly how Q&A and other mentioned items are connected somewhere, into a table to be processed, by their type. One generated q&a for each block and another for statistics, such as containing some words more or less than other documents, compared to their length, etc.
```

## Virtual Tables, Multi‑Role Chapters, and Provider‑Linked Processing

This chapter rewrites the previous creative format into the same structural style we used earlier: second‑level chapter, escaped sub‑blocks, clear subsections, and consistent Markdown formatting.

### Hashed and Classed Tags as Virtual Tables

Hashed (`#Thread`) and classed (`.Class`) tags automatically form **virtual tables**.  
These tables are not stored physically; they are computed by scanning all tags in the document set.

Each tag becomes a **row** in every table corresponding to its classes and hashes.

```
#TagName.classA.classB
#TagName#Thread
#TagName.classA#Thread
```

- `.classA` → row appears in table *classA*  
- `.classB` → row appears in table *classB*  
- `#Thread` → row appears in thread‑table *Thread*  

These tables can be accessed in a **SQL‑like manner** by any provider:

```
SELECT * FROM classA WHERE TagName LIKE "Chapter%"
```

The system does not require server‑side scripting or access rights.  
The server is open‑source and read‑only; clients cannot corrupt it.  
Heavy reasoning is delegated to **AI processors** that perform metadeductions.

### Multi‑Role Chapters: Question, Instruction, Answer

A single chapter may contain:

- a **Question**  
- an **Instruction**  
- an **Answer**  

Different providers choose which role to activate, but the **same answer** is reused.

```
[/Chapter id="Sorting"]
  (/Question.classQ)
    How do I sort items alphabetically?
  (Question/)

  (/Instruction.classI)
    Sort items alphabetically using provider rules.
  (Instruction/)

  (/Answer.classA)
    Alphabetical sorting is performed by comparing Unicode codepoints.
  (Answer/)
[Chapter/]
```

Providers may run in:

- **Q→A mode**  
- **I→A mode**  
- **A‑only mode**  

### Superchapter Prefixing and Title Injection

A superchapter may define a **prefix rule** that applies to all incorporated titles.

```
[/SuperChapter prefix="→ "]
  [/ChapterRef]Sorting[ChapterRef/]
  [/ChapterRef]Filtering[ChapterRef/]
[SuperChapter/]
```

Rendered:
    → Sorting
    → Filtering


A triggered extension may add:

- prefix  
- two line feeds  
- or two trailing spaces  

This allows list‑style summaries or prefixed outlines.

### Dual Provider Formats per Chapter Class

Each chapter may belong to two provider classes:

- **QA** (question–answer generation)  
- **Stats** (statistical analysis)  

```
[/Chapter id="MergeSort" class="QA Stats"]
  (/Question.classQ)
    What is merge sort?
  (Question/)

  (/Instruction.classI)
    Explain merge sort in a single paragraph.
  (Instruction/)

  (/Answer.classA)
    Merge sort divides the list into halves, recursively sorts each half, and merges them.
  (Answer/)
[Chapter/]
```

#### Provider 1: Q&A Generator

    SELECT Question, Answer FROM QA WHERE Chapter="MergeSort"

Produces:
    Q: What is merge sort?
    A: Merge sort divides the list into halves, recursively sorts each half, and merges them.


#### Provider 2: Statistics Generator

    SELECT WordCount, RareWords, Density FROM Stats WHERE Chapter="MergeSort"

Produces:


#### Provider 2: Statistics Generator

    SELECT WordCount, RareWords, Density FROM Stats WHERE Chapter="MergeSort"

Produces:
    Word count: 17
    Rare words: 0
    Density: 0.0

(which can be converted to various cards associating resource by it's local id, and it's variables, and sometimes by global id like url or general example)

### Why This System Works

- Tags become **database rows**  
- Classes become **virtual tables**  
- Providers act like **SQL engines**  
- Chapters carry **multiple semantic roles**  
- Superchapters can **rewrite or prefix** content  
- AI processors perform **metadeductions**  
- Open‑source servers remain **safe** because clients cannot mutate tables  

This creates a **queryable, AI‑processable, multi‑role document universe**.
