use std::process::{Command, Stdio};
use std::thread;
use std::io::{BufRead, BufReader};
use tauri::Emitter;
use serde_json;

#[tauri::command]
fn greet(name: &str) -> String {
    format!("Hello, {}! You've been greeted from Rust!", name)
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_opener::init())
        .setup(|app| {
            let app_handle = app.handle().clone();
            
            thread::spawn(move || {
                start_python_backend(app_handle);
            });
            
            Ok(())
        })
        .invoke_handler(tauri::generate_handler![greet])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}

fn start_python_backend(app_handle: tauri::AppHandle) {
    let project_root = std::path::PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .join("../../");
    
    let python_path = if cfg!(target_os = "windows") {
        "python"
    } else {
        "python3"
    };
    
    let mut child = match Command::new(python_path)
        .arg("main.py")
        .current_dir(project_root.join("backend"))
        .env("TAURI_ENV", "true")
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .spawn()
    {
        Ok(child) => child,
        Err(e) => {
            eprintln!("Failed to start Python backend: {}", e);
            return;
        }
    };
    
    if let Some(stdout) = child.stdout.take() {
        let app_handle_clone = app_handle.clone();
        thread::spawn(move || {
            let reader = BufReader::new(stdout);
            for line in reader.lines() {
                if let Ok(line) = line {
                    process_log_line(&app_handle_clone, &line);
                }
            }
        });
    }
    
    if let Some(stderr) = child.stderr.take() {
        let app_handle_clone = app_handle.clone();
        thread::spawn(move || {
            let reader = BufReader::new(stderr);
            for line in reader.lines() {
                if let Ok(line) = line {
                    process_log_line(&app_handle_clone, &line);
                }
            }
        });
    }
    
    let _ = child.wait();
}

fn process_log_line(app_handle: &tauri::AppHandle, line: &str) {
    if line.starts_with("__TAURI_LOG__") {
        if let Some(json_str) = line.strip_prefix("__TAURI_LOG__") {
            if let Ok(log_data) = serde_json::from_str::<serde_json::Value>(json_str) {
                let _ = app_handle.emit("log-event", log_data);
            }
        }
    }
}
