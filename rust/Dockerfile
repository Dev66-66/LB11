# Stage 1: builder — compile the binary
FROM rust:1.75 AS builder

WORKDIR /app

# Cache dependencies by building a dummy project first
COPY Cargo.toml Cargo.lock ./
RUN mkdir src && echo 'fn main(){}' > src/main.rs && cargo build --release

# Now build the real source
COPY src ./src
RUN touch src/main.rs && cargo build --release


# Stage 2: minimal runtime image
FROM debian:bookworm-slim

COPY --from=builder /app/target/release/textutil /usr/local/bin/textutil

ENTRYPOINT ["textutil"]
CMD ["--help"]
