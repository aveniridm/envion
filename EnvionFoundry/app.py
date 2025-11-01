from flask import Flask, request, jsonify, send_from_directory
import subprocess, os, tempfile

app = Flask(__name__)
UPLOAD_DIR = "uploads"
OUTPUT_DIR = "output"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.route('/')
def index():
    return open("index.html").read()

@app.route('/style.css')
def css():
    return open("style.css").read(), 200, {'Content-Type': 'text/css'}

@app.route('/script.js')
def js():
    return open("script.js").read(), 200, {'Content-Type': 'application/javascript'}

@app.route('/process', methods=['POST'])
def process_audio():
    file = request.files.get('file')
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    in_path = os.path.join(UPLOAD_DIR, file.filename)
    file.save(in_path)

    base = os.path.splitext(file.filename)[0]
    out_dir = os.path.join(OUTPUT_DIR, base)
    os.makedirs(out_dir, exist_ok=True)

    # FFmpeg pipeline (EnvionSeeder v5 logic)
    cmd = f'''
    export LC_ALL=C;
    input="{in_path}";
    slices="{out_dir}/slices";
    pitch="{out_dir}/slices_pitchup";
    mkdir -p "$slices" "$pitch";
    for i in $(seq 0 9); do
      start=$(awk -v n="$i" 'BEGIN{{printf "%.1f", n*3.0}}');
      out=$(printf "%s/{base}_slice_%02d.wav" "$slices" "$((i+1))");
      ffmpeg -hide_banner -loglevel error -ss "$start" -t 3 -i "$input" \
        -acodec pcm_s16le -ar 48000 -ac 2 "$out";
    done;
    for f in "$slices"/*.wav; do
      name=$(basename "$f");
      ffmpeg -y -hide_banner -loglevel error -i "$f" \
        -af "asetrate=384000,aresample=48000,atempo=1.6,
             afade=t=in:st=0:d=0.1,
             afade=t=out:st=1.5:d=1.5,
             volume=4.0,
             alimiter=limit=1.0,
             dynaudnorm=f=250:g=20" \
        "$pitch/$name";
    done;
    '''

    try:
        subprocess.run(cmd, shell=True, check=True)
        return jsonify({"success": True, "output_dir": out_dir})
    except subprocess.CalledProcessError as e:
        return jsonify({"error": "Processing failed", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8000)
