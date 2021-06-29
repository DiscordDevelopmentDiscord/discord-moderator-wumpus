FROM python:3.9-slim

# Set this both here and in pyproject.toml
ENV POETRY_VERSION=1.0.0
ENV APP_ROOT=/app

# set to production to disable dev package installs
ENV APP_ENV="development"

RUN pip install "poetry==$POETRY_VERSION"
RUN poetry config virtualenvs.create false

# Handle dependency caching in a sane manner
WORKDIR $APP_ROOT/
COPY poetry.lock pyproject.toml $APP_ROOT/
RUN poetry install --no-interaction --no-ansi $(test "$APP_ENV" = "production" && echo "--no-dev")

# Copy in the rest of the project
COPY . $APP_ROOT/

# Run the bot (headless/override, better for actual app run and IDE-based development)
CMD python -m bot