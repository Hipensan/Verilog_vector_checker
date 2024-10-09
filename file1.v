module file1(   // Half adder
    input i_A,
    input i_B,
    input i_C,
    output o_C,     // carry
    output o_S      // sum
);



assign o_C = (i_A & i_B) | ((i_A ^ i_B) & i_C);
assign o_S = i_A ^ i_B ^ i_C;

endmodule

