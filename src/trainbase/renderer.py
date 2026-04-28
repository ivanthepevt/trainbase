from IPython.display import display, Markdown, HTML, clear_output
import ipywidgets as widgets


def render_blocks(chapter_id, blocks, progress_store):
    start_index = progress_store.get_block_index(chapter_id)

    def advance(i):
        progress_store.set_block_index(chapter_id, i + 1)
        run_block(i + 1)

    def run_block(i):
        if i >= len(blocks):
            progress_store.mark_chapter_complete(chapter_id)
            display(Markdown(f"## ✅ Chapter completed: `{chapter_id}`"))
            return

        block = blocks[i]
        block_type = block["type"]
        content = block["content"]

        if block_type == "markdown":
            display(Markdown(content))
            progress_store.set_block_index(chapter_id, i + 1)
            run_block(i + 1)

        elif block_type == "video":
            render_video(content)
            progress_store.set_block_index(chapter_id, i + 1)
            run_block(i + 1)

        elif block_type == "quiz":
            render_quiz(
                content,
                on_success=lambda points: (
                    progress_store.add_score(chapter_id, points),
                    advance(i)
                )
            )

        elif block_type == "reflect":
            render_reflect(
                content,
                on_success=lambda answer, points: (
                    progress_store.save_reflection(
                        chapter_id,
                        content.get("question", ""),
                        answer
                    ),
                    progress_store.add_score(chapter_id, points),
                    advance(i)
                )
            )

        else:
            display(Markdown(f"Unsupported block type: `{block_type}`"))
            advance(i)

    run_block(start_index)


def render_video(data):
    url = data.get("url", "")
    video_id = extract_youtube_id(url)

    if not video_id:
        display(Markdown(f"[Open video]({url})"))
        return

    display(HTML(f"""
    <div style="margin: 16px 0;">
      <iframe width="720" height="405"
        src="https://www.youtube.com/embed/{video_id}"
        title="YouTube video player"
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


def render_quiz(q, on_success):
    out = widgets.Output()

    display(Markdown(f"### Quiz\n**{q.get('question', '')}**"))

    q_type = q.get("type", "mcq")
    points = int(q.get("points", 1))

    if q_type == "mcq":
        answer_widget = widgets.RadioButtons(options=q.get("options", []))
    elif q_type == "text":
        answer_widget = widgets.Text(placeholder="Type your answer")
    else:
        display(Markdown(f"Unsupported quiz type: `{q_type}`"))
        return

    button = widgets.Button(description="Submit", button_style="success")

    def check(_):
        with out:
            clear_output()

            user_answer = answer_widget.value
            correct_answer = q.get("answer", "")

            if q_type == "text":
                user_answer = user_answer.strip()
                correct_answer = str(correct_answer).strip()

                if str(q.get("case_sensitive", "true")).lower() == "false":
                    user_answer = user_answer.lower()
                    correct_answer = correct_answer.lower()

            if user_answer == correct_answer:
                print(f"✅ Correct (+{points} point)")
                on_success(points)
            else:
                print("❌ Not yet. Try again.")

    button.on_click(check)
    display(answer_widget, button, out)


def render_reflect(r, on_success):
    out = widgets.Output()

    question = r.get("question", "")
    min_words = int(r.get("min_words", 20))
    points = int(r.get("points", 1))

    display(Markdown(f"### Reflection\n**{question}**"))

    text_area = widgets.Textarea(
        placeholder="Write your response here...",
        layout=widgets.Layout(width="100%", height="140px")
    )
    button = widgets.Button(description="Submit reflection", button_style="info")

    def check(_):
        with out:
            clear_output()
            answer = text_area.value.strip()
            word_count = len(answer.split())

            if word_count >= min_words:
                print(f"✅ Reflection submitted ({word_count} words, +{points} point)")
                on_success(answer, points)
            else:
                print(f"❌ Please write at least {min_words} words. Current: {word_count}")

    button.on_click(check)
    display(text_area, button, out)
