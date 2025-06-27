// #define _GNU_SOURCE
// #include <stdio.h>
// #include <stdlib.h>
// #include <string.h>
// #include <unistd.h>
// #include <fcntl.h>
// #include <sys/types.h>
// #include <sys/wait.h>
// #include <time.h>
// #include <stdbool.h>
// #include <sys/stat.h>
// #include <stdint.h>
// #include <linux/perf_event.h>
// #include <sys/ioctl.h>
// #include <sys/syscall.h>
// #include <errno.h>

// // Global variables for UPS function
// double setpoint_dram_power = 0;
// double pre_ipc = 0;
// int dual_cap = 0;
// int init = 1;
// double current_uf = 2.2;
// double current_uf_2 = 2.2;
// double step = 0.1;

// #define MAX_RAPL_FILES 10

// // Structure to store monitoring data
// typedef struct {
//     double time;
//     double dram_power;
//     double ipc;
// } PowerIpcData;

// typedef struct {
//     double result;
// } ThreadData;


// // Array to store paths to DRAM energy files
// char *dram_energy_files[MAX_RAPL_FILES];
// int num_dram_files = 0;


// // Function to discover DRAM energy files from RAPL
// void discover_dram_rapl_files() {
//     const char *rapl_base_path = "/sys/class/powercap";
//     char path[256];

//     for (int socket_id = 0; socket_id < 2; socket_id++) {  // Adjust the range based on your system
//         snprintf(path, sizeof(path), "%s/intel-rapl:%d/intel-rapl:%d:0/energy_uj", rapl_base_path, socket_id, socket_id);
//         if (access(path, F_OK) == 0) {  // Check if the file exists
//             dram_energy_files[num_dram_files] = strdup(path);
//             if (dram_energy_files[num_dram_files] == NULL) {
//                 perror("Error duplicating path string");
//                 exit(EXIT_FAILURE);
//             }
//             num_dram_files++;
//         }
//     }

//     if (num_dram_files == 0) {
//         fprintf(stderr, "No DRAM energy files found. Exiting.\n");
//         exit(EXIT_FAILURE);
//     }
// }

// // Function to read DRAM energy
// double read_dram_energy() {
//     double total_energy = 0;
//     char buffer[32];

//     for (int i = 0; i < num_dram_files; i++) {
//         int fd = open(dram_energy_files[i], O_RDONLY);
//         if (fd < 0) {
//             perror("Error opening energy file");
//             continue;
//         }

//         ssize_t bytes_read = read(fd, buffer, sizeof(buffer) - 1);
//         if (bytes_read <= 0) {
//             perror("Error reading energy file");
//             close(fd);
//             continue;
//         }
//         buffer[bytes_read] = '\0';  // Null-terminate the string
//         close(fd);

//         total_energy += atof(buffer) / 1000000;  // Convert to joules
//     }

//     return total_energy;
// }


// // Function to collect IPC using `perf stat`
// double collect_ipc() {
//     // Use a shorter sampling duration and simplify perf output
//     FILE *fp = popen("perf stat -e instructions,cycles -a --no-merge --field-separator=, -x, sleep 0.01 2>&1", "r");
//     if (fp == NULL) {
//         perror("Error running perf command");
//         return -1;
//     }

//     char line[256];
//     double instructions = 0;
//     double cycles = 0;

//     // Directly parse specific fields for instructions and cycles
//     while (fgets(line, sizeof(line), fp) != NULL) {
//         if (strstr(line, "instructions")) {
//             sscanf(line, "%lf,", &instructions); // Extract the first value
//         } else if (strstr(line, "cycles")) {
//             sscanf(line, "%lf,", &cycles); // Extract the first value
//         }
//     }

//     pclose(fp);

//     // Return IPC if cycles > 0, else return 0
//     return (cycles > 0) ? (instructions / cycles) : 0;
// }


// void ups(double dram_power, double ipc) {
//     if (init==1) {
//         setpoint_dram_power = dram_power;
//         pre_ipc = ipc;
//         init=0;
        
//     }

//     else {
//         double delta_dram_power = dram_power - setpoint_dram_power;
//         double delta_ipc = ipc - pre_ipc;
        
//         // state 1: decrement uf
//         if (fabs(delta_dram_power) <= setpoint_dram_power * 0.05) {
//             if (current_uf > 1.2) {
//                 current_uf -= step;
//                 char command[128];
//                 // current_uf = 1.2;
//                 snprintf(command, sizeof(command), "sudo /home/cc/power/GPGPU/script/power_util/set_uncore_freq.sh %.2f %.2f", current_uf, current_uf);
//                 (void)system(command);
//             }
//         } 
//         // state 3
//         else if (delta_dram_power > setpoint_dram_power * 0.05) {
//             pre_ipc = ipc;
//             setpoint_dram_power = dram_power;
//             current_uf = 2.2;
//             if (dual_cap==1){
//                 (void)system("sudo /home/cc/power/GPGPU/script/power_util/set_uncore_freq.sh 2.2 2.2");
//             }
//             else{
//                 (void)system("sudo /home/cc/power/GPGPU/script/power_util/set_uncore_freq.sh 2.2 1.2");
//             }
               
//         } else if (delta_dram_power < -setpoint_dram_power * 0.05) {
//             // state 3
//             if (delta_ipc >= pre_ipc * 0.05) {
//                 setpoint_dram_power = dram_power;
//                 pre_ipc = ipc;
//                 current_uf = 2.2;
//                 if (dual_cap==1){
//                     (void)system("sudo /home/cc/power/GPGPU/script/power_util/set_uncore_freq.sh 2.2 2.2");
//                 }
//                 else{
//                     (void)system("sudo /home/cc/power/GPGPU/script/power_util/set_uncore_freq.sh 2.2 1.2");
//                 }
//             } 
//             // state 2: increment
//             else if (delta_ipc < -pre_ipc * 0.05) {
//                 pre_ipc = ipc;
//                 char command[128];
//                 if (current_uf < 2.2) {
//                     current_uf += step;
//             }
//                 if (dual_cap==1){
//                     current_uf = 2.2;
//                     snprintf(command, sizeof(command), "sudo /home/cc/power/GPGPU/script/power_util/set_uncore_freq.sh %.2f %.2f", current_uf, current_uf);
//                     (void)system(command);
//                 }
//                 else{
//                     current_uf = 2.2;
//                     snprintf(command, sizeof(command), "sudo /home/cc/power/GPGPU/script/power_util/set_uncore_freq.sh %.2f %.2f", current_uf, 1.2);
//                     (void)system(command);
//                 }
//             }
//         }
//     }
    
// }


// void *read_energy_thread(void *arg) {
//     ThreadData *data = (ThreadData *)arg;
//     data->result = read_dram_energy();
//     pthread_exit(NULL);
// }

// void *collect_ipc_thread(void *arg) {
//     ThreadData *data = (ThreadData *)arg;
//     data->result = collect_ipc();
//     pthread_exit(NULL);
// }


// // Main monitoring function
// void monitor_dram_power_and_ipc(int pid, const char *output_csv, double interval) {
//     size_t buffer_size = 1000;  // Initial buffer size
//     PowerIpcData *data = malloc(buffer_size * sizeof(PowerIpcData));
//     if (data == NULL) {
//         perror("Error allocating memory");
//         exit(EXIT_FAILURE);
//     }

//     int count = 0;
//     struct timespec start_time;
//     clock_gettime(CLOCK_MONOTONIC, &start_time);  // Get the starting time

//     double initial_energy = read_dram_energy();

//     while (kill(pid, 0) == 0) {
//         struct timespec current_time;
//         clock_gettime(CLOCK_MONOTONIC, &current_time);

//         double elapsed_time_ms = (current_time.tv_sec - start_time.tv_sec) * 1000.0
//                                  + (current_time.tv_nsec - start_time.tv_nsec) / 1e6;
//         double elapsed_time_sec = elapsed_time_ms / 1000.0;

//         pthread_t energy_thread, ipc_thread;
//         ThreadData energy_data, ipc_data;

//         if (pthread_create(&energy_thread, NULL, read_energy_thread, &energy_data) != 0) {
//             perror("Error creating energy thread");
//             // free(data);
//             exit(EXIT_FAILURE);
//         }

//         if (pthread_create(&ipc_thread, NULL, collect_ipc_thread, &ipc_data) != 0) {
//             perror("Error creating IPC thread");
//             pthread_cancel(energy_thread);
//             free(data);
//             exit(EXIT_FAILURE);
//         }

//         pthread_join(energy_thread, NULL);
//         pthread_join(ipc_thread, NULL);

//         double final_energy = energy_data.result;
//         double ipc = ipc_data.result;

//         double energy_diff = final_energy - initial_energy;
//         double dram_power = energy_diff / interval;
//         initial_energy = final_energy;

//         // Resize the buffer if needed
//         if (count >= buffer_size) {
//             buffer_size *= 2;  // Double the buffer size
//             PowerIpcData *new_data = realloc(data, buffer_size * sizeof(PowerIpcData));
//             if (new_data == NULL) {
//                 perror("Error reallocating memory");
//                 free(data);
//                 exit(EXIT_FAILURE);
//             }
//             data = new_data;
//         }

//         data[count].time = elapsed_time_sec;
//         data[count].dram_power = dram_power;
//         data[count].ipc = ipc;
//         count++;

//         //ups(dram_power, ipc);
//     }

//     // Write all collected data to CSV
//     FILE *fp = fopen(output_csv, "w");
//     if (fp == NULL) {
//         perror("Error opening CSV file");
//         free(data);
//         exit(EXIT_FAILURE);
//     }

//     fprintf(fp, "Time (s),DRAM Power (W),IPC\n");
//     for (int i = 0; i < count; i++) {
//         fprintf(fp, "%.4f,%.2f,%.2f\n", data[i].time, data[i].dram_power, data[i].ipc);
//     }

//     fclose(fp);
//     free(data);
// }

// int main(int argc, char *argv[]) {
//     int pid = -1;
//     const char *output_csv = NULL;
//     double interval = 0.1;

//     // Discover DRAM energy files before running the main logic
//     discover_dram_rapl_files();

//     // Check if the arguments are in the form --param=value
//     for (int i = 1; i < argc; i++) {
//         if (strncmp(argv[i], "--pid=", 6) == 0) {
//             pid = atoi(argv[i] + 6);
//         } else if (strncmp(argv[i], "--output_csv=", 13) == 0) {
//             output_csv = argv[i] + 13;
//         } else if (strncmp(argv[i], "--dual_cap=", 11) == 0) {
//             dual_cap = atoi(argv[i] + 11);
//         } else {
//             fprintf(stderr, "Unknown argument: %s\n", argv[i]);
//             exit(EXIT_FAILURE);
//         }
//     }

//     // Check if the required arguments were provided
//     if (pid == -1 || output_csv == NULL) {
//         fprintf(stderr, "Usage: %s --pid=<PID> --output_csv=<output_csv>\n", argv[0]);
//         exit(EXIT_FAILURE);
//     }

//     monitor_dram_power_and_ipc(pid, output_csv, interval);

//     // Free allocated memory for file paths
//     for (int i = 0; i < num_dram_files; i++) {
//         free(dram_energy_files[i]);
//     }

//     return 0;
// }


#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <time.h>
#include <stdbool.h>
#include <sys/stat.h>
#include <stdint.h>
#include <linux/perf_event.h>
#include <sys/ioctl.h>
#include <sys/syscall.h>
#include <errno.h>

// Global variables for UPS function
double setpoint_dram_power = 0;
double pre_ipc = 0;
int dual_cap = 0;
int init = 1;
double current_uf = 2.2;
double current_uf_2 = 2.2;
double step = 0.1;

#define MAX_RAPL_FILES 10

// Structure to store monitoring data
typedef struct {
    double time;
    double dram_power;
    double ipc;
} PowerIpcData;

// Array to store paths to DRAM energy files
char *dram_energy_files[MAX_RAPL_FILES];
int num_dram_files = 0;

// Function to discover DRAM energy files from RAPL
void discover_dram_rapl_files() {
    const char *rapl_base_path = "/sys/class/powercap";
    char path[256];

    for (int socket_id = 0; socket_id < 2; socket_id++) {  // Adjust the range based on your system
        snprintf(path, sizeof(path), "%s/intel-rapl:%d/intel-rapl:%d:0/energy_uj", rapl_base_path, socket_id, socket_id);
        if (access(path, F_OK) == 0) {  // Check if the file exists
            dram_energy_files[num_dram_files] = strdup(path);
            if (dram_energy_files[num_dram_files] == NULL) {
                perror("Error duplicating path string");
                exit(EXIT_FAILURE);
            }
            num_dram_files++;
        }
    }

    if (num_dram_files == 0) {
        fprintf(stderr, "No DRAM energy files found. Exiting.\n");
        exit(EXIT_FAILURE);
    }
}

// Function to read DRAM energy
double read_dram_energy() {
    double total_energy = 0;
    char buffer[32];

    for (int i = 0; i < num_dram_files; i++) {
        int fd = open(dram_energy_files[i], O_RDONLY);
        if (fd < 0) {
            perror("Error opening energy file");
            continue;
        }

        ssize_t bytes_read = read(fd, buffer, sizeof(buffer) - 1);
        if (bytes_read <= 0) {
            perror("Error reading energy file");
            close(fd);
            continue;
        }
        buffer[bytes_read] = '\0';  // Null-terminate the string
        close(fd);

        total_energy += atof(buffer) / 1000000;  // Convert to joules
    }

    return total_energy;
}

// Function to call the perf_event_open syscall
// static int perf_event_open(struct perf_event_attr *hw_event, pid_t pid, int cpu, int group_fd, unsigned long flags) {
//     return syscall(__NR_perf_event_open, hw_event, pid, cpu, group_fd, flags);
// }

// // Function to collect IPC using perf_event_open
// double collect_ipc() {
//     uint64_t total_instr = 0;
//     uint64_t total_cycles = 0;
//     int core_count = 0;

//     // Iterate over even-numbered cores (0, 2, 4, ..., 158)
//     for (int cpu = 0; cpu < 160; cpu += 2) {
//         struct perf_event_attr pe_instr, pe_cycles;
//         memset(&pe_instr, 0, sizeof(struct perf_event_attr));
//         memset(&pe_cycles, 0, sizeof(struct perf_event_attr));

//         // Configure for instructions retired
//         pe_instr.type = PERF_TYPE_HARDWARE;
//         pe_instr.size = sizeof(struct perf_event_attr);
//         pe_instr.config = PERF_COUNT_HW_INSTRUCTIONS;
//         pe_instr.disabled = 1;
//         pe_instr.exclude_kernel = 0;
//         pe_instr.exclude_hv = 0;

//         // Configure for CPU cycles
//         pe_cycles.type = PERF_TYPE_HARDWARE;
//         pe_cycles.size = sizeof(struct perf_event_attr);
//         pe_cycles.config = PERF_COUNT_HW_CPU_CYCLES;
//         pe_cycles.disabled = 1;
//         pe_cycles.exclude_kernel = 0;
//         pe_cycles.exclude_hv = 0;

//         int fd_instr = perf_event_open(&pe_instr, -1, cpu, -1, 0);
//         if (fd_instr == -1) {
//             fprintf(stderr, "Error opening perf event for instructions on CPU %d: %s\n", cpu, strerror(errno));
//             continue;
//         }

//         int fd_cycles = perf_event_open(&pe_cycles, -1, cpu, -1, 0);
//         if (fd_cycles == -1) {
//             fprintf(stderr, "Error opening perf event for cycles on CPU %d: %s\n", cpu, strerror(errno));
//             close(fd_instr);
//             continue;
//         }

//         // Enable the counters
//         ioctl(fd_instr, PERF_EVENT_IOC_RESET, 0);
//         ioctl(fd_cycles, PERF_EVENT_IOC_RESET, 0);
//         ioctl(fd_instr, PERF_EVENT_IOC_ENABLE, 0);
//         ioctl(fd_cycles, PERF_EVENT_IOC_ENABLE, 0);

//         // Wait for a short duration to accumulate data
//         usleep(50000);  // 50 ms

//         // Disable the counters
//         ioctl(fd_instr, PERF_EVENT_IOC_DISABLE, 0);
//         ioctl(fd_cycles, PERF_EVENT_IOC_DISABLE, 0);

//         uint64_t count_instr = 0;
//         uint64_t count_cycles = 0;

//         read(fd_instr, &count_instr, sizeof(uint64_t));
//         read(fd_cycles, &count_cycles, sizeof(uint64_t));

//         // Close the file descriptors
//         close(fd_instr);
//         close(fd_cycles);

//         // Aggregate the counts if valid
//         if (count_cycles > 0) {
//             total_instr += count_instr;
//             total_cycles += count_cycles;
//             core_count++;
//         }
//     }

//     // Return the average IPC value
//     return (total_cycles > 0 && core_count > 0) ? ((double)total_instr / total_cycles) : 0;
// }


// Function to collect IPC using `perf stat`
double collect_ipc() {
    FILE *fp = popen("perf stat -e instructions,cycles -a --no-merge --field-separator=, -x, sleep 0.05 2>&1", "r");
    if (fp == NULL) {
        perror("Error running perf command");
        return -1;
    }

    char line[256];
    double instructions = 0;
    double cycles = 0;

    while (fgets(line, sizeof(line), fp) != NULL) {
        if (strstr(line, "instructions")) {
            instructions = atof(strtok(line, ","));
        }
        if (strstr(line, "cycles")) {
            cycles = atof(strtok(line, ","));
        }
    }

    pclose(fp);
    return (cycles > 0) ? (instructions / cycles) : 0;
}

void ups(double dram_power, double ipc) {
    if (init==1) {
        setpoint_dram_power = dram_power;
        pre_ipc = ipc;
        init=0;
        
    }

    else {
        double delta_dram_power = dram_power - setpoint_dram_power;
        double delta_ipc = ipc - pre_ipc;
        
        // state 1: decrement uf
        if (fabs(delta_dram_power) <= setpoint_dram_power * 0.05) {
            if (current_uf > 1.2) {
                current_uf -= step;
                char command[128];
                // current_uf = 1.2;
                snprintf(command, sizeof(command), "sudo /home/cc/power/GPGPU/script/power_util/set_uncore_freq.sh %.2f %.2f", current_uf, current_uf);
                (void)system(command);
            }
        } 
        // state 3
        else if (delta_dram_power > setpoint_dram_power * 0.05) {
            pre_ipc = ipc;
            setpoint_dram_power = dram_power;
            current_uf = 2.2;
            if (dual_cap==1){
                (void)system("sudo /home/cc/power/GPGPU/script/power_util/set_uncore_freq.sh 2.2 2.2");
            }
            else{
                (void)system("sudo /home/cc/power/GPGPU/script/power_util/set_uncore_freq.sh 2.2 1.2");
            }
               
        } else if (delta_dram_power < -setpoint_dram_power * 0.05) {
            // state 3
            if (delta_ipc >= pre_ipc * 0.05) {
                setpoint_dram_power = dram_power;
                pre_ipc = ipc;
                current_uf = 2.2;
                if (dual_cap==1){
                    (void)system("sudo /home/cc/power/GPGPU/script/power_util/set_uncore_freq.sh 2.2 2.2");
                }
                else{
                    (void)system("sudo /home/cc/power/GPGPU/script/power_util/set_uncore_freq.sh 2.2 1.2");
                }
            } 
            // state 2: increment
            else if (delta_ipc < -pre_ipc * 0.05) {
                pre_ipc = ipc;
                char command[128];
                if (current_uf < 2.2) {
                    current_uf += step;
            }
                if (dual_cap==1){
                    current_uf = 2.2;
                    snprintf(command, sizeof(command), "sudo /home/cc/power/GPGPU/script/power_util/set_uncore_freq.sh %.2f %.2f", current_uf, current_uf);
                    (void)system(command);
                }
                else{
                    current_uf = 2.2;
                    snprintf(command, sizeof(command), "sudo /home/cc/power/GPGPU/script/power_util/set_uncore_freq.sh %.2f %.2f", current_uf, 1.2);
                    (void)system(command);
                }
            }
        }
    }
    
}


// Main monitoring function
void monitor_dram_power_and_ipc(int pid, const char *output_csv, double interval) {
    PowerIpcData *data = malloc(1000000 * sizeof(PowerIpcData));  // Allocate space for storing data
    if (data == NULL) {
        perror("Error allocating memory");
        exit(EXIT_FAILURE);
    }

    int count = 0;
    struct timespec start_time;
    clock_gettime(CLOCK_MONOTONIC, &start_time);  // Get the starting time

    double initial_energy = read_dram_energy();

    while (kill(pid, 0) == 0) {
        struct timespec current_time;
        clock_gettime(CLOCK_MONOTONIC, &current_time);

        // Calculate elapsed time in milliseconds
        double elapsed_time_ms = (current_time.tv_sec - start_time.tv_sec) * 1000.0 
                                 + (current_time.tv_nsec - start_time.tv_nsec) / 1e6;

        double elapsed_time_sec = elapsed_time_ms / 1000.0;  // Convert to seconds for CSV output

        double final_energy = read_dram_energy();
        double energy_diff = final_energy - initial_energy;

        double dram_power = energy_diff / (0.2);
        initial_energy = final_energy;

        double ipc = collect_ipc();  // Replace `0` with the appropriate CPU number

        if (count < 10000000) {
            data[count].time = elapsed_time_sec;
            data[count].dram_power = dram_power;
            data[count].ipc = ipc;
            count++;
        } else {
            printf("Buffer full, consider increasing the buffer size.\n");
            break;
        }
      
        // struct timespec t1, t2;
        // clock_gettime(CLOCK_MONOTONIC, &t1);  // Start time
        
        ups(dram_power, ipc);
        
        // clock_gettime(CLOCK_MONOTONIC, &t2);  // End time
    
        // double elapsed_time = (t2.tv_sec - t1.tv_sec) + 
        //                       (t2.tv_nsec - t1.tv_nsec) / 1000000000.0;
        // printf("Average time per call using clock_gettime(): %f seconds\n", elapsed_time);


          // usleep((useconds_t)(0.14 * 1e6));  
    }

    // Write all collected data to CSV
    FILE *fp = fopen(output_csv, "w");
    if (fp == NULL) {
        perror("Error opening CSV file");
        free(data);
        exit(EXIT_FAILURE);
    }

    fprintf(fp, "Time (s),DRAM Power (W),IPC\n");
    for (int i = 0; i < count; i++) {
        fprintf(fp, "%.4f,%.2f,%.2f\n", data[i].time, data[i].dram_power, data[i].ipc);
    }

    fclose(fp);
    free(data);
}

int main(int argc, char *argv[]) {
    int pid = -1;
    const char *output_csv = NULL;
    double interval = 0.1;

    // Discover DRAM energy files before running the main logic
    discover_dram_rapl_files();

    // Check if the arguments are in the form --param=value
    for (int i = 1; i < argc; i++) {
        if (strncmp(argv[i], "--pid=", 6) == 0) {
            pid = atoi(argv[i] + 6);
        } else if (strncmp(argv[i], "--output_csv=", 13) == 0) {
            output_csv = argv[i] + 13;
        } else if (strncmp(argv[i], "--dual_cap=", 11) == 0) {
            dual_cap = atoi(argv[i] + 11);
        } else {
            fprintf(stderr, "Unknown argument: %s\n", argv[i]);
            exit(EXIT_FAILURE);
        }
    }

    // Check if the required arguments were provided
    if (pid == -1 || output_csv == NULL) {
        fprintf(stderr, "Usage: %s --pid=<PID> --output_csv=<output_csv>\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    monitor_dram_power_and_ipc(pid, output_csv, interval);

    // Free allocated memory for file paths
    for (int i = 0; i < num_dram_files; i++) {
        free(dram_energy_files[i]);
    }

    return 0;
}
