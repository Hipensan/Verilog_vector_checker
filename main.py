import re
from collections import defaultdict

def extract_signals(verilog_code):
    # wire, reg 등의 신호 선언을 찾는 정규식
    signal_pattern = r"(?<!\w)(input|output|wire|reg)?\s*(\[\d+:\d+\])?\s*(\w+)\s*(;|,\s*|$)"
    
    signals = {}

    # 정규식으로 모든 신호를 찾음
    matches = re.findall(signal_pattern, verilog_code, re.MULTILINE)

    for match in matches:
        vector_size = match[1]  # [2:0] 또는 None
        signal_name = match[2]   # 신호 이름

        # 벡터 크기 없는 경우 스칼라 신호로 처리
        if vector_size == '':
            vector_size = '[0:0]'

        # 인스턴스 이름과 endmodule 필터링
        if signal_name not in ['endmodule'] and not re.match(r'adder\d*', signal_name):
            # 신호 추가
            if signal_name not in signals:
                signals[signal_name] = vector_size
    
    return signals

def extract_instance_mappings(verilog_code):
    # 인스턴스 포트 매핑을 찾는 정규식 개선
    instance_pattern = r"(\w+)\s+(\w+)\s*\(([^)]+)\);"  # 인스턴스 내의 포트 매핑 추출
    port_pattern = r"\.(\w+)\s*\(\s*(\w+(\[\d+:\d+\]|\[\d+\])?)\s*\)"  # 각 포트 매핑 추출

    instance_mappings = defaultdict(list)

    # 포트 매핑을 추출
    matches = re.findall(instance_pattern, verilog_code)
    for match in matches:
        module_name = match[0]  # 모듈 이름 (예: file1)
        instance_name = match[1]  # 인스턴스 이름 (예: adder0)
        ports_block = match[2]  # 포트 매핑 블록 (예: .i_A(i_A[0]), .i_B(i_B[0]) ...)

        ports = re.findall(port_pattern, ports_block)
        for port in ports:
            port_name = port[0]  # 포트 이름 (예: i_A)
            signal_name = port[1]  # 신호 이름 (예: i_A[0])
            instance_mappings[signal_name].append(port_name)  # 인스턴스화된 신호에 대한 포트 매핑 추가

    return instance_mappings

def check_instance_signals(signals, instance_mappings):
    missing_signals = []

    # 모든 인스턴스 신호를 확인
    for signal_name in instance_mappings.keys():
        if signal_name not in signals:
            missing_signals.append(signal_name)

    return missing_signals

def read_verilog_file(filepath):
    with open(filepath, 'r') as f:
        return f.read()

def main(file_path):
    # 파일 읽기
    verilog_code = read_verilog_file(file_path)
    
    # 신호 추출
    signals = extract_signals(verilog_code)
    
    # 인스턴스 매핑 추출
    instance_mappings = extract_instance_mappings(verilog_code)

    # 인스턴스에서 사용된 신호가 선언된 신호인지 확인
    missing_signals = check_instance_signals(signals, instance_mappings)

    # 찾은 신호 출력
    print("찾은 신호:")
    for signal, size in signals.items():
        print(f"Signal: {signal}, Size: {size}")
    
    if missing_signals:
        print("\n다음 신호들이 선언되지 않았습니다:")
        for missing in missing_signals:
            print(f"Missing Signal: {missing}")
    else:
        print("\n모든 인스턴스 신호가 정상적으로 선언되었습니다.")

# 예시 실행
file_path = 'file2.v'  # 테스트할 Verilog 파일 경로
main(file_path)
