module file2(   // 2bit adder
    input [1:0] i_A,
    input [1:0] i_B,
    output [2:0] o_S      // sum
);



file1 adder0(   
    .i_A(i_A[0]),
    .i_B(i_B[0]),
    .i_C(1'b0),
    .o_C(carry[0]),     
    .o_S(o_S[0])      
);

file1 adder1(   
    .i_A(i_A[1]),
    .i_B(i_B[1]),
    .i_C(carry[0]),
    .o_C(carry[1]),     
    .o_S(o_S[1])      
);

assign o_S[2] = carry[1];

endmodule




