from IPython.display import display, Markdown, HTML, clear_output
import ipywidgets as widgets


def render_blocks(chapter_id, blocks, progress_store):
    """
    NEW BEHAVIOR:
    - render ALL blocks immediately
    - NO blocking
    - user can answer in any order
    """

    for block in blocks:
        block_type = block["type"]
        content = block["content"]

        if block_type == "markdown":
            display(Markdown(content))

        elif block_type == "video":
            render_video(content)

        elif block_type == "quiz":
            render_quiz(content, chapter_id, progress_store)

        elif block_type == "reflect":
            render_reflect(content, chapter_id, progress_store)

        else:
            display(Markdown(f"Unsupported block type: `{block_type}`"))

    # mark complete immediately (you chose no blocking)
    progress_store.mark_chapter_complete(chapter_id)
    display(Markdown(f"## ✅ Chapter loaded: `{chapter_id}`"))


# ======================
# VIDEO
# ======================
def render_video(data):
    url = data.get("url", "")
    vid = extract_youtube_id(url)

    if not vid:
        display(Markdown(f"[Open video]({url})"))
        return

    display(HTML(f"""
    <div style="margin:20px 0;">
      <iframe width="720" height="405"
        src="https://www.youtube.com/embed/{vid}"
        frameborder="0"
        allowfullscreen>
      </iframe>
    </div>
    """))


def extract_youtube_id(url):
    if "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0]
    if "watch?v=" in url:
        return url.split("watch?v=")[1].split("&")[0]
    return None


# ======================
# QUIZ (FIXED UI)
# ======================
def render_quiz(q, chapter_id, progress_store):
    display(Markdown(f"### Quiz\n**{q.get('question', '')}**"))

    out = widgets.Output()

    points = int(q.get("points", 1))
    q_type = q.get("type", "mcq")

    # FIX: force clean layout
    layout = widgets.Layout(width="100%")

    if q_type == "mcq":
        # FIX: wrap text nicely
        options = [(opt, opt) for opt in q.get("options", [])]

        answer_widget = widgets.RadioButtons(
            options=options,
            layout=layout,
            style={'description_width': 'initial'}
        )

    elif q_type == "text":
        answer_widget = widgets.Text(
            placeholder="Type your answer",
            layout=layout
        )

    else:
        display(Markdown(f"Unsupported quiz type: `{q_type}`"))
        return

    button = widgets.Button(
        description="Submit",
        button_style="success",
        layout=widgets.Layout(width="200px")
    )

    def check(_):
        with out:
            clear_output()

            user = answer_widget.value
            correct = q.get("answer", "")

            if q_type == "text":
                user = user.strip()
                correct = str(correct).strip()

                if str(q.get("case_sensitive", "true")).lower() == "false":
                    user = user.lower()
                    correct = correct.lower()

            if user == correct:
                print(f"✅ Correct (+{points})")
                progress_store.add_score(chapter_id, points)
            else:
                print("❌ Not yet. Try again.")

    button.on_click(check)

    display(answer_widget)
    display(button)
    display(out)


# ======================
# REFLECTION (FIXED UX)
# ======================
def render_reflect(r, chapter_id, progress_store):
    display(Markdown(f"### 💡 Reflection\n**{r.get('question', '')}**"))

    out = widgets.Output()

    text_area = widgets.Textarea(
        placeholder="Write your response here...",
        layout=widgets.Layout(width="100%", height="150px")
    )

    button = widgets.Button(
        description="Submit reflection",
        button_style="info"
    )

    min_words = int(r.get("min_words", 20))
    points = int(r.get("points", 1))

    def check(_):
        with out:
            clear_output()

            answer = text_area.value.strip()
            wc = len(answer.split())

            if wc >= min_words:
                print(f"✅ Saved ({wc} words, +{points})")

                progress_store.save_reflection(
                    chapter_id,
                    r.get("question", ""),
                    answer
                )
                progress_store.add_score(chapter_id, points)

            else:
                print(f"❌ Need at least {min_words} words (now {wc})")

    button.on_click(check)

    display(text_area)
    display(button)
    display(out)
