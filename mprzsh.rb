$_task = ENV['TASK']

if $_task != nil then
  puts "Imported task #{$_task} from environment"
end

def tasks
  return Dir[File.join("*", "*.cpp")].map do |x| /#{File.join("(.+)", "\\1\\.cpp")}/.match(x) end.delete_if do |x| (not x.is_a?(MatchData)) or x[1] == nil end.map do |x| x[1] end
end

def task(t = nil)
  if t == nil then
    return $_task
  else
    $_task = t
    ENV['TASK'] = $_task
  end
end

def check(options = "")
  if $_task == nil then
    raise 'Task not defined'
  end
  check_cmd = "python qtest.py #{$_task}" + " " + options
  system(check_cmd)
end

def edit
  if $_task == nil then
    raise 'Task not defined'
  end
  if not Dir.exists? $_task then
    Dir.mkdir $_task
  end
  system("vim #{File.join("#{$_task}", "#{$_task}.cpp")}")
end

def tests
  if $_task == nil then
    raise 'Task not defined'
  end
  return Dir[File.join("#{$_task}","*.in")].map { |x| /#{File.join("#{$_task}", "(.+)\\.in")}/.match(x)[1] }
end

def test(*names)
  if $_task == nil then
    raise 'Task not defined'
  end
  if not Dir.exists? $_task then
    Dir.mkdir $_task
  end
  names.each do |ref|
    system("vim #{File.join("#{$_task}", "#{ref}.in")} #{File.join("#{$_task}", "#{ref}.out")}")
  end
end
