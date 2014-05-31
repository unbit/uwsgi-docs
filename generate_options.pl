chdir $ARGV[0];

print <<'EOF';
uWSGI Options
^^^^^^^^^^^^^

This is an automatically generated reference list of the uWSGI options.

It is the same output you can get via the ``--help`` option.

This page is probably the worst way to understand uWSGI for newbies. If you are still learning how the project
works, you should read the various quickstarts and tutorials.

EOF


my $title = 'uWSGI core';
print $title."\n";
print '=' x length($title);
print "\n";
generate_doc('core/uwsgi.c');

opendir PLUGINS,'plugins';
while(my $d = readdir(PLUGINS)) {
	next if $d =~ /^\./;
	next unless -d 'plugins/'.$d;
	my $d_verbose = 'plugin: '.$d;
	print "\n".$d_verbose."\n";
	print '=' x length($d_verbose);
	print "\n";
	scan_dir('plugins/'.$d);
}

sub scan_dir {
	my ($path) = @_;
	if (-f $path) {
		if ($path =~ /\.(c|cc|m)$/) {
			generate_doc($path);
		}
	}
	elsif (-d $path) {
		opendir DIR, $path;
		while(my $d = readdir(DIR)) {
			next if $d =~ /^\./;
			scan_dir($path.'/'.$d);
		}
	}
}

sub generate_doc {
	my ($filename) = @_;
	open FILE,$filename;
	while(<FILE>) {
		chomp;
		if ($_ =~ /{.*\,.*\,.*\,.*\,.*\,.*\,.*}/) {
			my ($option, $type, $shortcut, $help, $func, $arg, $flags) = parse($_);
			next unless $option;
			next if $option eq 'NULL';
			print '----'.$option."\n";
			print '*' x length($option);
			print "\n";
			print '``argument``: '.$type."\n\n";
			if ($shortcut) {
				print '``shortcut``: -'.$shortcut."\n\n";
			}
			if ($func) {
				print '``parser``: '.$func."\n\n";
			}
			if ($flags) {
				print '``flags``: '.$flags."\n\n";
			}
			print "\n\n";
			print $help."\n\n";
		}
	}
	close(FILE);
}

sub parse {
	my ($line) = @_;
	my @letters = split //,$line;
	my $is_quoted = 0;
	my $is_escaped = 0;
	my $has_started = 0;
	my $has_ended = 0;
	my @result = ();
	my @items = ();
	foreach(@letters) {
		if (!$has_started) {
			if ($_ eq '{') {
				$has_started = 1;
			}
			next;
		}
		if (!$is_quoted) {
			if ($_ eq '"' or $_ eq "'") {
				$is_quoted = $_;
			}
			elsif ($_ eq '}') {
				$has_ended = 1;
				push @items, trim(join('', @result));
				last;
			}
			elsif ($_ eq ',') {
				push @items, trim(join('', @result));
				@result = ();
			}
			else {
				push @result,$_;
			}
		}
		elsif ($is_quoted) {
			if (!$is_escaped) {
				if ($_ eq $is_quoted) {
                                	$is_quoted = 0;
                        	}
				elsif ($_ eq '\\') {
					$is_escaped = 1;
				}
				else {
					push @result, $_;		
				}
			}
			else {
				push @result, $_;		
				$is_escaped = 0;
			}
		}
	}
	if ($has_ended) {
		return @items;
	}
	return ();
}

sub trim {
	my ($s) = @_;
	$s =~ s/^\s+//;
	$s =~ s/\s+$//;
	$s =~ s/\(char \*\)//g;
	return $s;
}
