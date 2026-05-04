from flask import Flask, request, jsonify

app = Flask(__name__)
seen = set()

ACCESS_MAP = {
    '0x1'     : 'ListDirectory / ReadData',
    '0x2'     : 'WriteData / AddFile',
    '0x4'     : 'AppendData / AddSubdir',
    '0x6'     : 'WriteData + AppendData',
    '0x8'     : 'ReadExtendedAttributes',
    '0x10'    : 'WriteExtendedAttributes',
    '0x20'    : 'Execute / Traverse',
    '0x40'    : 'DeleteChild',
    '0x80'    : 'ReadAttributes',
    '0x100'   : 'WriteAttributes',
    '0x10000' : 'Delete',
    '0x20000' : 'ReadControl',
    '0x40000' : 'ChangePermissions',
    '0x80000' : 'TakeOwnership',
    '0x120089': 'Read',
    '0x120116': 'Write',
    '0x1200a0': 'Execute',
    '0x1f01ff': 'FullControl',
}

SKIP = {'0x80', '0x100', '0x20000'}

SUSPICIOUS = ['powershell', 'cmd', 'python', 'nc.exe', 'meterpreter',
              'psexec', 'wscript', 'cscript', 'rundll32', 'mshta']

NOISE_PROCESSES = {
    'msmpeng.exe', 'svchost.exe', 'searchindexer.exe',
    'searchprotocolhost.exe', 'trustedinstaller.exe',
    'tiworker.exe', 'wuauclt.exe', 'spoolsv.exe',
}

@app.route('/token/<baitid>/fim', methods=['POST'])
def trigger(baitid):
    try:
        data = request.get_json(force=True, silent=True)

        if not data:
            print('[!] No JSON body received')
            return '', 400

        # --- Field extraction with safe defaults ---
        event_time = data.get('event_time', 'unknown')
        user       = data.get('user',       'unknown')
        path       = data.get('path',       'unknown')
        process    = data.get('process',    'unknown')
        access_raw = data.get('access',     '')

        ip = request.remote_addr

        # Normalise access mask to lowercase hex string
        access = access_raw.strip().lower() if access_raw else ''

        # Extract just the exe name from full process path
        process_name = process.split('\\')[-1].lower() if process else 'unknown'

        # Resolve human-readable label; fall back to raw value
        access_label = ACCESS_MAP.get(access, access or 'unknown')

        # --- Filters ---
        if access in SKIP:
            return '', 204

        if process_name in NOISE_PROCESSES:
            return '', 204

        # Deduplication (mirrors the PowerShell-side dedup key)
        key = f"{user}|{path}|{access}|{event_time}"
        if key in seen:
            return '', 204
        seen.add(key)

        # --- Alert ---
        suspicious_flag = any(s in process_name for s in SUSPICIOUS)
        flag_str = '  *** SUSPICIOUS PROCESS ***' if suspicious_flag else ''

        print()
        print('=' * 55)
        print(f'        FOLDER ACCESS DETECTED{flag_str}')
        print('=' * 55)
        print(f'  BaitId  : {baitid}')
        print(f'  User    : {user}')
        print(f'  Path    : {path}')
        print(f'  Process : {process_name}  <== Tool Used')
        print(f'  Access  : {access_label}')
        print(f'  IP      : {ip}')
        print(f'  Time    : {event_time}')
        print('=' * 55)

    except Exception as e:
        print(f'[!] Error processing FIM callback: {e}')

    return '', 204


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
