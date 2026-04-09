use std::env;
use std::process;

fn count_text(input: &str) -> String {
    let words = if input.trim().is_empty() {
        0
    } else {
        input.split_whitespace().count()
    };
    let chars = input.chars().count();
    let lines = if input.is_empty() {
        0
    } else {
        input.lines().count()
    };
    format!(
        r#"{{"command":"count","input":{},"words":{},"chars":{},"lines":{}}}"#,
        json_string(input),
        words,
        chars,
        lines
    )
}

fn reverse_text(input: &str) -> String {
    let result: String = input.chars().rev().collect();
    format!(
        r#"{{"command":"reverse","input":{},"result":{}}}"#,
        json_string(input),
        json_string(&result)
    )
}

fn upper_text(input: &str) -> String {
    let result = input.to_uppercase();
    format!(
        r#"{{"command":"upper","input":{},"result":{}}}"#,
        json_string(input),
        json_string(&result)
    )
}

fn lower_text(input: &str) -> String {
    let result = input.to_lowercase();
    format!(
        r#"{{"command":"lower","input":{},"result":{}}}"#,
        json_string(input),
        json_string(&result)
    )
}

fn json_string(s: &str) -> String {
    let escaped = s
        .replace('\\', "\\\\")
        .replace('"', "\\\"")
        .replace('\n', "\\n")
        .replace('\r', "\\r")
        .replace('\t', "\\t");
    format!("\"{}\"", escaped)
}

fn error_json(msg: &str) -> String {
    format!(r#"{{"error":{}}}"#, json_string(msg))
}

fn run(args: &[String]) -> Result<String, String> {
    if args.len() < 2 {
        return Err(error_json("Usage: textutil <command> <text>"));
    }
    let command = &args[1];
    if args.len() < 3 {
        return Err(error_json(&format!(
            "Command '{}' requires a text argument",
            command
        )));
    }
    let input = &args[2];
    match command.as_str() {
        "count" => Ok(count_text(input)),
        "reverse" => Ok(reverse_text(input)),
        "upper" => Ok(upper_text(input)),
        "lower" => Ok(lower_text(input)),
        "--help" | "-h" => Err(error_json(
            "Usage: textutil <command> <text>. Commands: count, reverse, upper, lower",
        )),
        other => Err(error_json(&format!("Unknown command: '{}'", other))),
    }
}

fn main() {
    let args: Vec<String> = env::args().collect();
    match run(&args) {
        Ok(output) => println!("{}", output),
        Err(err) => {
            eprintln!("{}", err);
            process::exit(1);
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn make_args(cmd: &str, text: &str) -> Vec<String> {
        vec!["textutil".to_string(), cmd.to_string(), text.to_string()]
    }

    fn make_cmd_only(cmd: &str) -> Vec<String> {
        vec!["textutil".to_string(), cmd.to_string()]
    }

    // --- count ---

    #[test]
    fn test_count_single_word() {
        let out = run(&make_args("count", "hello")).unwrap();
        assert!(out.contains(r#""words":1"#));
    }

    #[test]
    fn test_count_two_words() {
        let out = run(&make_args("count", "hello world")).unwrap();
        assert!(out.contains(r#""words":2"#));
    }

    #[test]
    fn test_count_five_words() {
        let out = run(&make_args("count", "one two three four five")).unwrap();
        assert!(out.contains(r#""words":5"#));
    }

    #[test]
    fn test_count_chars() {
        let out = run(&make_args("count", "hello")).unwrap();
        assert!(out.contains(r#""chars":5"#));
    }

    #[test]
    fn test_count_chars_with_spaces() {
        let out = run(&make_args("count", "hi yo")).unwrap();
        assert!(out.contains(r#""chars":5"#));
    }

    #[test]
    fn test_count_single_line() {
        let out = run(&make_args("count", "hello world")).unwrap();
        assert!(out.contains(r#""lines":1"#));
    }

    #[test]
    fn test_count_empty_string() {
        let out = run(&make_args("count", "")).unwrap();
        assert!(out.contains(r#""words":0"#));
        assert!(out.contains(r#""chars":0"#));
        assert!(out.contains(r#""lines":0"#));
    }

    #[test]
    fn test_count_command_field() {
        let out = run(&make_args("count", "test")).unwrap();
        assert!(out.contains(r#""command":"count""#));
    }

    #[test]
    fn test_count_input_field() {
        let out = run(&make_args("count", "test")).unwrap();
        assert!(out.contains(r#""input":"test""#));
    }

    // --- reverse ---

    #[test]
    fn test_reverse_basic() {
        let out = run(&make_args("reverse", "hello")).unwrap();
        assert!(out.contains(r#""result":"olleh""#));
    }

    #[test]
    fn test_reverse_palindrome() {
        let out = run(&make_args("reverse", "racecar")).unwrap();
        assert!(out.contains(r#""result":"racecar""#));
    }

    #[test]
    fn test_reverse_single_char() {
        let out = run(&make_args("reverse", "a")).unwrap();
        assert!(out.contains(r#""result":"a""#));
    }

    #[test]
    fn test_reverse_empty_string() {
        let out = run(&make_args("reverse", "")).unwrap();
        assert!(out.contains(r#""result":"""#));
    }

    #[test]
    fn test_reverse_command_field() {
        let out = run(&make_args("reverse", "abc")).unwrap();
        assert!(out.contains(r#""command":"reverse""#));
    }

    // --- upper ---

    #[test]
    fn test_upper_lowercase_input() {
        let out = run(&make_args("upper", "hello")).unwrap();
        assert!(out.contains(r#""result":"HELLO""#));
    }

    #[test]
    fn test_upper_mixed_case() {
        let out = run(&make_args("upper", "HeLLo WoRLd")).unwrap();
        assert!(out.contains(r#""result":"HELLO WORLD""#));
    }

    #[test]
    fn test_upper_command_field() {
        let out = run(&make_args("upper", "x")).unwrap();
        assert!(out.contains(r#""command":"upper""#));
    }

    // --- lower ---

    #[test]
    fn test_lower_uppercase_input() {
        let out = run(&make_args("lower", "HELLO")).unwrap();
        assert!(out.contains(r#""result":"hello""#));
    }

    #[test]
    fn test_lower_mixed_case() {
        let out = run(&make_args("lower", "HeLLo WoRLd")).unwrap();
        assert!(out.contains(r#""result":"hello world""#));
    }

    #[test]
    fn test_lower_command_field() {
        let out = run(&make_args("lower", "X")).unwrap();
        assert!(out.contains(r#""command":"lower""#));
    }

    // --- error cases ---

    #[test]
    fn test_unknown_command_returns_error() {
        let result = run(&make_args("foobar", "text"));
        assert!(result.is_err());
        assert!(result.unwrap_err().contains(r#""error""#));
    }

    #[test]
    fn test_no_args_returns_error() {
        let args = vec!["textutil".to_string()];
        let result = run(&args);
        assert!(result.is_err());
    }

    #[test]
    fn test_command_without_text_returns_error() {
        let result = run(&make_cmd_only("count"));
        assert!(result.is_err());
        assert!(result.unwrap_err().contains(r#""error""#));
    }

    #[test]
    fn test_unknown_command_error_message() {
        let result = run(&make_args("xyz", "hi"));
        let err = result.unwrap_err();
        assert!(err.contains("Unknown command"));
    }
}
