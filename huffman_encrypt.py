import heapq
import os
from functools import total_ordering


import pyAesCrypt
from os import stat, remove

@total_ordering
class NodeOfHeapifyTree:
	def __init__(self, alpha, occurence):
		self.alpha = alpha
		self.occurence = occurence
		self.left = None
		self.right = None

	# defining comparators less_than and equals
       def __eq__(self, different):
		if(different == None):
			return False
		if(not isinstance(different, NodeOfHeapifyTree)):
			return False
		return self.occurence == different.occurence
  
	def __lt__(self, different):
		return self.occurence < different.occurence

	


class CodeTree:
	def __init__(self, source):
		self.source = source
		self.heap_list = []
		self.codes_list = {}
		self.inverse_map = {}

	# functions for compression:

	

	def heapify(self, frequency):
		for vertex in frequency:
			vertex = NodeOfHeapifyTree(value, frequency[vertex])
			heapq.heappush(self.heap_list, vertex)

	def vertices_merging(self):
		while(len(self.heap_list)>1):
			vertex1 = heapq.heappop(self.heap_list)
			vertex2 = heapq.heappop(self.heap_list)

			formed= NodeOfHeapifyTree(None, vertex1.occurence + node2.occurence)
			formed.left = vertex1
			formed.right = vertex2

			heapq.heappush(self.heap_list, formed)


	def make_codes_helper(self, root, current_code):
		if(root == None):
			return

		if(root.char != None):
			self.codes[root.char] = current_code
			self.reverse_mapping[current_code] = root.char
			return

		self.make_codes_helper(root.left, current_code + "0")
		self.make_codes_helper(root.right, current_code + "1")


	def make_codes(self):
		root = heapq.heappop(self.heap)
		current_code = ""
		self.make_codes_helper(root, current_code)


	def get_encoded_text(self, text):
		encoded_text = ""
		for character in text:
			encoded_text += self.codes[character]
		return encoded_text


	def pad_encoded_text(self, encoded_text):
		extra_padding = 8 - len(encoded_text) % 8
		for i in range(extra_padding):
			encoded_text += "0"

		padded_info = "{0:08b}".format(extra_padding)
		encoded_text = padded_info + encoded_text
		return encoded_text


	def get_byte_array(self, padded_encoded_text):
		if(len(padded_encoded_text) % 8 != 0):
			print("Encoded text not padded properly")
			exit(0)

		b = bytearray()
		for i in range(0, len(padded_encoded_text), 8):
			byte = padded_encoded_text[i:i+8]
			b.append(int(byte, 2))
		return b


	def compress(self):
		filename, file_extension = os.source.splitext(self.source)
		output_source = filename + ".compressed"

		with open(self.source, 'r+') as file, open(output_source, 'wb') as output:
			text = file.read()
			text = text.rstrip()

			frequency = self.make_frequency_dict(text)
			self.make_heap(frequency)
			self.merge_nodes()
			self.make_codes()

			encoded_text = self.get_encoded_text(text)
			padded_encoded_text = self.pad_encoded_text(encoded_text)

			b = self.get_byte_array(padded_encoded_text)
			output.write(bytes(b))

		print("Compressed")
		return output_source


	""" functions for decompression: """


	def remove_padding(self, padded_encoded_text):
		padded_info = padded_encoded_text[:8]
		extra_padding = int(padded_info, 2)

		padded_encoded_text = padded_encoded_text[8:] 
		encoded_text = padded_encoded_text[:-1*extra_padding]

		return encoded_text

	def decode_text(self, encoded_text):
		current_code = ""
		decoded_text = ""

		for bit in encoded_text:
			current_code += bit
			if(current_code in self.reverse_mapping):
				character = self.reverse_mapping[current_code]
				decoded_text += character
				current_code = ""

		return decoded_text


	def decompress(self, input_source):
		filename, file_extension = os.source.splitext(self.source)
		output_source = filename + "_decompressed" + ".txt"

		with open(input_source, 'rb') as file, open(output_source, 'w') as output:
			bit_string = ""

			byte = file.read(1)
			while(len(byte) > 0):
				byte = ord(byte)
				bits = bin(byte)[2:].rjust(8, '0')
				bit_string += bits
				byte = file.read(1)

			encoded_text = self.remove_padding(bit_string)

			decompressed_text = self.decode_text(encoded_text)
			
			output.write(decompressed_text)

		print("Decompressed")
		return output_source
  
xx=[]  
while(1):
    l=int(input("Press 1 for to Encrypt and Huffman encode:\nPress 2 to get the desired input file from list of encrypted files:\nPress 3 to halt:"))
    if(l==1):    
        x=input("Enter Filename:")
        xx.append(x)
        source = r'C:\Users\Prerna Atwal\Downloads\New folder'+ str(x)
        print(source)

        huffobject = CodeTree(source)

        output_source = huffobject.compress()
        print("hello"+output_source)
        # encryption/decryption buffer size
        bS = 64 * 1024
        pwd = input("Enter the password to encrypt the file:") # encryption of file data.txt
        with open(x[1:x.find(".")]+'.compressed', 'rb') as fileinputobject:
            with open(x[1:x.find(".")]+'.compressed.encrypt', 'wb') as fileoutputobject:
                pyAesCrypt.encryptStream(fileinputobject, fileoutputobject, pwd, bS)# get encrypted file size
        encFileSize = stat(x[1:x.find(".")]+'.compressed.encrypt').st_size
        print(encFileSize) #prints file size
        print(stat(x[1:x.find(".")]+'.compressed').st_size)
    elif(l==2):
        
        bS = 64 * 1024
        ll=input("Enter filename to decrypt: ")
        pwd=input("enter password to decrypt: ")
        
        source = r'C:\Users\Prerna Atwal\Downloads\New folder'+ str(ll)
        huffobject = CodeTree(source)
        lll=ll[1:ll.find(".")]
        eFSize = stat(ll[1:ll.find(".")]+'.compressed.encrypt').st_size       
        with open(lll+'.compressed.encrypt', 'rb') as fileinputobject:
            with open(lll+'decrypt.compressed', 'wb') as fileoutputobject:
                try:
                    pyAesCrypt.decryptStream(fileinputobject, fileoutputobject, pwd, bS, eFSize)
                except ValueError:
# remove output file on error
                    remove(lll+'decrypt.compressed')
                    
        huffobject.decompress(lll+".compressed")
    else:
        break        
